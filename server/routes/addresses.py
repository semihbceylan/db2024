from flask import Blueprint, jsonify, request
from mysql.connector import Error

from utils.get_db_connection import get_db_connection
from moralis import evm_api

from dotenv import load_dotenv
import os

addresses = Blueprint('addresses', __name__)

@addresses.route("/<string:address>", methods=['GET'])
def get_address(address):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM addresses WHERE address = '{address}'")
        data = cursor.fetchone()
        if not data:
            return jsonify({"error": "Address not found"}), 404
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@addresses.route("/<string:address>", methods=['DELETE'])
def delete_address(address):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM addresses WHERE address = '{address}'")
        if cursor.rowcount == 0:
            return jsonify({"error": "Address not found"}), 404
        cursor.execute(f"SELECT block_number, chain_id FROM blocks WHERE miner = '{address}'")
        blocks_to_delete = cursor.fetchall()
        blocks_deleted = 0
        transactions_deleted = 0
        for block in blocks_to_delete:
            chain_id = block["chain_id"]
            block_number = block["block_number"]
            cursor.execute(f"DELETE FROM transactions WHERE chain_id = {chain_id} AND block_number = {block_number}") # in case of error we need to first delete the trasactions 
            transactions_deleted += cursor.rowcount
            cursor.execute(f"DELETE FROM blocks WHERE chain_id = {chain_id} AND block_number = {block_number}")
            blocks_deleted += cursor.rowcount
        cursor.execute(f"DELETE FROM transactions WHERE from_address = '{address}' OR to_address = '{address}'")
        transactions_deleted += cursor.rowcount
        cursor.execute(f"DELETE FROM nfts WHERE owner = '{address}'")
        nfts_deleted = cursor.rowcount
        return jsonify({
            "message": "Address and related data deleted successfully",
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

@addresses.route("/<string:address>/", methods=['POST'])
def add_address(address):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        native_dollar_balance = 0
        erc20_count = 0
        erc20_dollar_balance = 0
        nft_count = 0
        
        cursor.execute("SELECT chain_id FROM chains")
        chains = cursor.fetchall()
        
        for chain in chains:
            chain_id = chain["chain_id"]

            tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY"), {
                "chain": f"0x{chain_id:x}",
                "address": address
            }))["result"]

            for token in tokens:
                if token["native_token"]:
                    native_dollar_balance += float(token["usd_value"] if token["usd_value"] else 0)
                else:
                    erc20_count += 1
                    erc20_dollar_balance += float(token["usd_value"] if token["usd_value"] else 0)

            nfts = (evm_api.nft.get_wallet_nfts(os.getenv("MORALIS_API_KEY"), {
                "chain": f"0x{chain_id:x}",
                "format": "decimal",
                "media_items": False,
                "address": address
            }))["result"]

            nft_count += len(nfts)

        sql = f"""
            INSERT INTO addresses (address, native_dollar_balance, erc20_count, erc20_dollar_balance, nft_count)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                native_dollar_balance = VALUES(native_dollar_balance),
                erc20_count = VALUES(erc20_count),
                erc20_dollar_balance = VALUES(erc20_dollar_balance),
                nft_count = VALUES(nft_count)
        """

        cursor.execute(sql, (
            address,
            round(float(native_dollar_balance), 18),
            int(erc20_count),
            round(float(erc20_dollar_balance), 18),
            int(nft_count)
        ))

        return jsonify({"message": "Address added/updated successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@addresses.route("/with-nfts/<string:address>/", methods=['POST'])
def full_add_address(address):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        native_dollar_balance = 0
        erc20_count = 0
        erc20_dollar_balance = 0
        nft_count = 0
        
        cursor.execute("SELECT chain_id FROM chains")
        chains = cursor.fetchall()
        
        for chain in chains:
            chain_id = chain["chain_id"]

            tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY"), {
                "chain": f"0x{chain_id:x}",
                "address": address
            }))["result"]

            for token in tokens:
                if token["native_token"]:
                    native_dollar_balance += float(token["usd_value"] if token["usd_value"] else 0)
                else:
                    erc20_count += 1
                    erc20_dollar_balance += float(token["usd_value"] if token["usd_value"] else 0)

            nfts = (evm_api.nft.get_wallet_nfts(os.getenv("MORALIS_API_KEY"), {
                "chain": f"0x{chain_id:x}",
                "format": "decimal",
                "media_items": False,
                "address": address
            }))["result"]

            nft_count += len(nfts)

            for nft in nfts:
                contract_address = nft["token_address"]
                token_id = nft["token_id"]
                contract_type = nft["contract_type"]

                if int(token_id) > 2**64 - 1: # token_id is too large to store in a BIGINT
                    nft_count -= 1
                    continue

                sql = f"""
                    INSERT IGNORE INTO nfts (chain_id, contract_address, token_id, owner, contract_type)
                    VALUES (%s, %s, %s, %s, %s)
                """

                cursor.execute(sql, (
                    int(chain_id),
                    contract_address,
                    int(token_id),
                    address,
                    contract_type
                ))

        sql = f"""
            INSERT INTO addresses (address, native_dollar_balance, erc20_count, erc20_dollar_balance, nft_count)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE 
                native_dollar_balance = VALUES(native_dollar_balance),
                erc20_count = VALUES(erc20_count),
                erc20_dollar_balance = VALUES(erc20_dollar_balance),
                nft_count = VALUES(nft_count)
        """

        cursor.execute(sql, (
            address,
            round(float(native_dollar_balance), 18),
            int(erc20_count),
            round(float(erc20_dollar_balance), 18),
            int(nft_count)
        ))

        return jsonify({"message": "Address added/updated and owned nfts added successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()