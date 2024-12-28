from flask import Blueprint, jsonify, request
from mysql.connector import Error

from utils.get_db_connection import get_db_connection
from moralis import evm_api

from dotenv import load_dotenv
import os

chains = Blueprint('chains', __name__)

@chains.route("/", methods=['GET'])
def get_chains ():
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM chains")
        data = cursor.fetchall()
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@chains.route("/<int:chain_id>", methods=['DELETE'])
def delete_chain(chain_id):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM chains WHERE chain_id = {chain_id}")
        if cursor.rowcount == 0:
            return jsonify({"error": "Chain not found"}), 404
        cursor.execute(f"DELETE FROM blocks WHERE chain_id = {chain_id}")
        blocks_deleted = cursor.rowcount
        cursor.execute(f"DELETE FROM transactions WHERE chain_id = {chain_id}")
        transactions_deleted = cursor.rowcount
        cursor.execute(f"DELETE FROM nfts WHERE chain_id = {chain_id}")
        nfts_deleted = cursor.rowcount
        connection.commit()
        
        cursor.execute("SELECT address FROM addresses")
        addresses = cursor.fetchall()

        cursor.execute("SELECT chain_id FROM chains")
        chains = cursor.fetchall()

        for address in addresses:
            address = address["address"]

            native_dollar_balance = 0
            erc20_count = 0
            erc20_dollar_balance = 0
            nft_count = 0
            
            for chain in chains:
                _chain_id = chain["chain_id"]

                tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY"), {
                    "chain": f"0x{_chain_id:x}",
                    "address": address
                }))["result"]

                for token in tokens:
                    if token["native_token"]:
                        native_dollar_balance += float(token["usd_value"] if token["usd_value"] else 0)
                    else:
                        erc20_count += 1
                        erc20_dollar_balance += float(token["usd_value"] if token["usd_value"] else 0)

                nfts = (evm_api.nft.get_wallet_nfts(os.getenv("MORALIS_API_KEY"), {
                    "chain": f"0x{_chain_id:x}",
                    "format": "decimal",
                    "media_items": False,
                    "address": address
                }))["result"]

                nft_count += len(nfts)

            sql = f"""
                UPDATE addresses
                SET
                    native_dollar_balance = %s,
                    erc20_count = %s,
                    erc20_dollar_balance = %s,
                    nft_count = %s
                WHERE address = '{address}' 
            """

            cursor.execute(sql, (
                round(float(native_dollar_balance), 18),
                int(erc20_count),
                round(float(erc20_dollar_balance), 18),
                int(nft_count)
            ))

        return jsonify({
            "message": "Chain and related data deleted, addresses updated successfully",
            "blocks_deleted": blocks_deleted,
            "transactions_deleted": transactions_deleted,
            "nfts_deleted": nfts_deleted
        }), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@chains.route("/", methods=["POST"])
def add_chain():
    data = request.json
    required_fields = ["chain_id", "chain_name", "native_currency", "explorer_url", "rpc_url"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    chain_id = data["chain_id"]
    chain_name = data["chain_name"]
    native_currency = data["native_currency"]
    explorer_url = data["explorer_url"]
    rpc_url = data["rpc_url"]
    
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM chains WHERE chain_id = {chain_id}")
        data = cursor.fetchone()
        if data:
            return jsonify({"error": "Chain already exists"}), 400
        query = "INSERT INTO chains (chain_id, chain_name, native_currency, explorer_url, rpc_url) VALUES (%s, %s, %s, %s, %s)"
        values = (chain_id, chain_name, native_currency, explorer_url, rpc_url)
        cursor.execute(query, values)
        return jsonify({"message": "Chain added successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@chains.route("/<int:chain_id>", methods=["PUT"])
def edit_chain(chain_id):
    data = request.json
    required_fields = ["chain_name", "native_currency", "explorer_url", "rpc_url"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM chains WHERE chain_id = {chain_id}")
        data = cursor.fetchone()
        if not data:
            return jsonify({"error": "Chain doesn't exists"}), 400
        query = "UPDATE chains SET chain_name = %s, native_currency = %s, explorer_url = %s, rpc_url = %s WHERE chain_id = %s"
        values = (data["chain_name"], data["native_currency"], data["explorer_url"], data["rpc_url"], chain_id)
        cursor.execute(query, values)
        return jsonify({"message": "Chain updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()