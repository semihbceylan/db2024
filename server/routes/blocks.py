from flask import Blueprint, jsonify, request
from mysql.connector import Error

from utils.get_db_connection import get_db_connection
from moralis import evm_api

from dotenv import load_dotenv
import os

blocks = Blueprint('blocks', __name__)

@blocks.route("/<int:chain_id>/<int:block_number>", methods=['GET'])
def get_block(chain_id, block_number):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM blocks WHERE chain_id = {chain_id} AND block_number = {block_number}")
        data = cursor.fetchone()
        if not data:
            return jsonify({"error": "Block not found"}), 404
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@blocks.route("/<int:chain_id>/<int:block_number>", methods=['DELETE'])
def delete_block(chain_id, block_number):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM blocks WHERE chain_id = {chain_id} AND block_number = {block_number}")
        if cursor.rowcount == 0:
            return jsonify({"error": "Block not found"}), 404
        cursor.execute(f"DELETE FROM transactions WHERE chain_id = {chain_id} AND block_number = {block_number}")
        transactions_deleted = cursor.rowcount
        return jsonify({
            "message": "BLock and related data deleted successfully",
            "transactions_deleted": transactions_deleted,
        }), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@blocks.route("/<int:chain_id>/<int:block_number>", methods=["POST"])
def add_block(chain_id, block_number):
    data = request.json
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM blocks WHERE chain_id = {chain_id} AND block_number = {block_number}")
        data = cursor.fetchone()
        if data:
            return jsonify({"error": "Block already exists"}), 400

        block = evm_api.block.get_block(os.getenv("MORALIS_API_KEY"), {
            "chain": f"0x{chain_id:x}",
            "block_number_or_hash": f"{block_number}"
        })

        block_hash = block["hash"]
        parent_hash = block["parent_hash"]
        miner = block["miner"]
        transactions = block["transactions"]
        timestamp = block["timestamp"]
        timestamp = f"{timestamp[:10]} {timestamp[11:19]}"

        # First, we need to insert the miner address to addresses table !

        cursor.execute("SELECT chain_id FROM chains")
        chains = cursor.fetchall()

        native_dollar_balance = 0
        erc20_count = 0
        erc20_dollar_balance = 0
        nft_count = 0
        
        for chain in chains:
            _chain_id = chain["chain_id"]

            tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY"), {
                "chain": f"0x{_chain_id:x}",
                "address": miner
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
                "address": miner
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
            miner,
            round(float(native_dollar_balance), 18),
            int(erc20_count),
            round(float(erc20_dollar_balance), 18),
            int(nft_count)
        ))

        sql = f"""
            INSERT INTO blocks (chain_id, block_number, block_hash, parent_hash, miner, tx_count, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            int(chain_id),
            int(block_number),
            block_hash,
            parent_hash,
            miner,
            int(len(transactions)),
            timestamp
        ))

        return jsonify({"message": "Block added successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@blocks.route("/full/<int:chain_id>/<int:block_number>", methods=['POST'])
def full_add_block(chain_id, block_number):
    data = request.json
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM blocks WHERE chain_id = {chain_id} AND block_number = {block_number}")
        data = cursor.fetchone()
        if data:
            return jsonify({"error": "Block already exists"}), 400

        block = evm_api.block.get_block(os.getenv("MORALIS_API_KEY"), {
            "chain": f"0x{chain_id:x}",
            "block_number_or_hash": f"{block_number}"
        })

        block_hash = block["hash"]
        parent_hash = block["parent_hash"]
        miner = block["miner"]
        transactions = block["transactions"]
        timestamp = block["timestamp"]
        timestamp = f"{timestamp[:10]} {timestamp[11:19]}"

        # First, we need to insert the miner address to addresses table !

        cursor.execute("SELECT chain_id FROM chains")
        chains = cursor.fetchall()

        native_dollar_balance = 0
        erc20_count = 0
        erc20_dollar_balance = 0
        nft_count = 0
        
        for chain in chains:
            _chain_id = chain["chain_id"]

            tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY"), {
                "chain": f"0x{_chain_id:x}",
                "address": miner
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
                "address": miner
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
            miner,
            round(float(native_dollar_balance), 18),
            int(erc20_count),
            round(float(erc20_dollar_balance), 18),
            int(nft_count)
        ))

        sql = f"""
            INSERT INTO blocks (chain_id, block_number, block_hash, parent_hash, miner, tx_count, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            int(chain_id),
            int(block_number),
            block_hash,
            parent_hash,
            miner,
            int(len(transactions)),
            timestamp
        ))

        for tx in transactions:
            _address = tx["from_address"]
            
            native_dollar_balance = 0
            erc20_count = 0
            erc20_dollar_balance = 0
            nft_count = 0
            
            for chain in chains:
                _chain_id = chain["chain_id"]

                tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY"), {
                    "chain": f"0x{_chain_id:x}",
                    "address": _address
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
                    "address": _address
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
                _address,
                round(float(native_dollar_balance), 18),
                int(erc20_count),
                round(float(erc20_dollar_balance), 18),
                int(nft_count)
            ))

            native_dollar_balance = 0
            erc20_count = 0
            erc20_dollar_balance = 0
            nft_count = 0
            
            for chain in chains:
                _chain_id = chain["chain_id"]

                tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY"), {
                    "chain": f"0x{_chain_id:x}",
                    "address": _address
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
                    "address": _address
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
                _address,
                round(float(native_dollar_balance), 18),
                int(erc20_count),
                round(float(erc20_dollar_balance), 18),
                int(nft_count)
            ))

            tx_hash = tx["hash"]
            from_address = tx["from_address"]
            to_address = tx["to_address"]
            value = tx["value"]

            # It is impossible the duplicate case for transactions, so we can directly insert the transaction
            sql = f"""
                INSERT INTO transactions (chain_id, tx_hash, from_address, to_address, block_number, value, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                int(chain_id),
                hash,
                from_address,
                to_address,
                int(block_number),
                float(value),
                timestamp
            ))

        return jsonify({"message": "Block added successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()