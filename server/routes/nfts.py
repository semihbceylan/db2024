from flask import Blueprint, jsonify, request
from mysql.connector import Error

from utils.get_db_connection import get_db_connection
from moralis import evm_api

from dotenv import load_dotenv
import os

nfts = Blueprint('nfts', __name__)

@nfts.route("/", methods=['GET'])
def get_nfts ():
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM nfts")
        data = cursor.fetchall()
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@nfts.route("/<int:chain_id>/<string:contract_address>", methods=['GET'])
def get_nft_contract(chain_id, contract_address):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM nfts WHERE chain_id = {chain_id} AND contract_address = '{contract_address}'")
        data = cursor.fetchall()
        if not data:
            return jsonify({"error": "NFT contract not found"}), 404
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@nfts.route("/<int:chain_id>/<string:contract_address>/<int:token_id>", methods=['GET'])
def get_nft(chain_id, contract_address, token_id):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM nfts WHERE chain_id = {chain_id} AND contract_address = '{contract_address}' AND token_id = {token_id}")
        data = cursor.fetchone()
        if not data:
            return jsonify({"error": "NFT not found"}), 404
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@nfts.route("/owner/<string:owner>", methods=['GET'])
def get_nfts_owned(owner):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM nfts WHERE owner = '{owner}'")
        data = cursor.fetchall()
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@nfts.route("/<int:chain_id>/<string:contract_address>", methods=['DELETE'])
def delete_nft_contract(chain_id, contract_address):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM nfts WHERE chain_id = {chain_id} AND contract_address = '{contract_address}'")
        nfts_deleted = cursor.rowcount
        if nfts_deleted == 0:
            return jsonify({"error": "NFT contract not found"}), 404
        return jsonify({
            "message": "NFT contract deleted",
            "nfts_deleted": nfts_deleted
        }), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@nfts.route("/<int:chain_id>/<string:contract_address>/<int:token_id>", methods=['DELETE'])
def delete_nft(chain_id, contract_address, token_id):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM nfts WHERE chain_id = {chain_id} AND contract_address = '{contract_address}' AND token_id = {token_id}")
        if cursor.rowcount == 0:
            return jsonify({"error": "NFT not found"}), 404
        return jsonify({"message": "NFT deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@nfts.route("/<int:chain_id>/<string:contract_address>", methods=['POST'])
def add_nft_contract(chain_id, contract_address):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        
        nfts= (evm_api.nft.get_contract_nfts(os.getenv("MORALIS_API_KEY_1"), {
            "chain": f"0x{chain_id:x}",
            "format": "decimal",
            "address": contract_address
        }))["result"]

        cursor.execute("SELECT chain_id FROM chains")
        chains = cursor.fetchall()

        for nft in nfts:
            name = nft["name"]
            token_id = nft["token_id"]
            owner = nft["owner_of"]
            contract_type = nft["contract_type"]

            # First, we need to insert the owner address to addresses table !

            native_dollar_balance = 0
            erc20_count = 0
            erc20_dollar_balance = 0
            nft_count = 0
            
            for chain in chains:
                _chain_id = chain["chain_id"]

                tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY_2"), {
                    "chain": f"0x{_chain_id:x}",
                    "address": owner
                }))["result"]

                for token in tokens:
                    if token["native_token"]:
                        native_dollar_balance += float(token["usd_value"] if token["usd_value"] else 0)
                    else:
                        erc20_count += 1
                        erc20_dollar_balance += float(token["usd_value"] if token["usd_value"] else 0)

                nfts = (evm_api.nft.get_wallet_nfts(os.getenv("MORALIS_API_KEY_3"), {
                    "chain": f"0x{_chain_id:x}",
                    "format": "decimal",
                    "media_items": False,
                    "address": owner
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
                owner,
                round(float(native_dollar_balance), 18),
                int(erc20_count),
                round(float(erc20_dollar_balance), 18),
                int(nft_count)
            ))

            sql = f"""
                INSERT INTO nfts (chain_id, contract_address, token_id, owner, contract_type, name) 
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    owner = VALUES(owner)
            """ # Other values cannot change

            cursor.execute(sql, (
                int(chain_id),
                contract_address,
                int(token_id),
                owner,
                contract_type,
                name
            ))

        return jsonify({"message": "NFT contract added"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@nfts.route("/<int:chain_id>/<string:contract_address>/<int:token_id>", methods=['POST'])
def add_nft(chain_id, contract_address, token_id):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        
        nfts= (evm_api.nft.get_contract_nfts(os.getenv("MORALIS_API_KEY_1"), {
            "chain": f"0x{chain_id:x}",
            "format": "decimal",
            "address": contract_address
        }))["result"]

        cursor.execute("SELECT chain_id FROM chains")
        chains = cursor.fetchall()

        for nft in nfts:
            name = nft["name"]
            _token_id = nft["token_id"]
            owner = nft["owner_of"]
            contract_type = nft["contract_type"]

            if (_token_id == token_id):
                continue

            # First, we need to insert the owner address to addresses table !

            native_dollar_balance = 0
            erc20_count = 0
            erc20_dollar_balance = 0
            nft_count = 0
            
            for chain in chains:
                _chain_id = chain["chain_id"]

                tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY_4"), {
                    "chain": f"0x{_chain_id:x}",
                    "address": owner
                }))["result"]

                for token in tokens:
                    if token["native_token"]:
                        native_dollar_balance += float(token["usd_value"] if token["usd_value"] else 0)
                    else:
                        erc20_count += 1
                        erc20_dollar_balance += float(token["usd_value"] if token["usd_value"] else 0)

                nfts = (evm_api.nft.get_wallet_nfts(os.getenv("MORALIS_API_KEY_5"), {
                    "chain": f"0x{_chain_id:x}",
                    "format": "decimal",
                    "media_items": False,
                    "address": owner
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
                owner,
                round(float(native_dollar_balance), 18),
                int(erc20_count),
                round(float(erc20_dollar_balance), 18),
                int(nft_count)
            ))

            sql = f"""
                INSERT INTO nfts (chain_id, contract_address, token_id, owner, contract_type, name) 
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    owner = VALUES(owner)
            """ # Other values cannot change

            cursor.execute(sql, (
                int(chain_id),
                contract_address,
                int(token_id),
                owner,
                contract_type,
                name
            ))

            break
        return jsonify({"message": "NFT added/updated"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@nfts.route("/", methods=['POST'])
def all_nfts():
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT address FROM addresses")
        addresses = cursor.fetchall()

        cursor.execute("SELECT chain_id FROM chains")
        chains = cursor.fetchall()

        for address in addresses:
            address = address["address"]

            for chain in chains:
                chain_id = chain["chain_id"]

                nfts = (evm_api.nft.get_wallet_nfts(os.getenv("MORALIS_API_KEY_1"), {
                    "chain": f"0x{chain_id:x}",
                    "format": "decimal",
                    "media_items": False,
                    "address": address
                }))["result"]

                for nft in nfts:
                    name = nft["name"]
                    contract_address = nft["token_address"]
                    token_id = nft["token_id"]
                    contract_type = nft["contract_type"]

                    if int(token_id) > 2**64 - 1: # token_id is too large to store in a BIGINT
                        continue

                    sql = f"""
                        INSERT INTO nfts (chain_id, contract_address, token_id, owner, contract_type, name)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                            owner = VALUES(owner)
                    """

                    cursor.execute(sql, (
                        int(chain_id),
                        contract_address,
                        int(token_id),
                        address,
                        contract_type,
                        name
                    ))

        return jsonify({"message": "NFTs reloaded"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()