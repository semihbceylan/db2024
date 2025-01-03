from flask import Blueprint, jsonify, request
from mysql.connector import Error

from utils.get_db_connection import get_db_connection
from moralis import evm_api

from dotenv import load_dotenv
import os

from routes.blocks import add_block
from routes.blocks import full_add_block

transactions = Blueprint('transactions', __name__)

@transactions.route("/<int:chain_id>/<string:tx_hash>", methods=['GET'])
def get_transaction(chain_id, tx_hash):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM transactions WHERE chain_id = {chain_id} AND tx_hash = '{tx_hash}'")
        data = cursor.fetchone()
        if not data:
            return jsonify({"error": "Transaction not found"}), 404
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@transactions.route("/<int:chain_id>/<string:tx_hash>", methods=['DELETE'])
def delete_transaction(chain_id, tx_hash):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM transactions WHERE chain_id = {chain_id} AND tx_hash = '{tx_hash}'")
        if cursor.rowcount == 0:
            return jsonify({"error": "Transaction not found"}), 404
        return jsonify({"message": "Transaction deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@transactions.route("/<int:chain_id>/<string:tx_hash>", methods=['POST'])
def add_transaction(chain_id, tx_hash):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM chains WHERE chain_id = {chain_id}")
        chain = cursor.fetchone()
        if not chain:
            return jsonify({"error": "Chain not found"}), 404
        
        cursor.execute(f"SELECT * FROM transactions WHERE chain_id = {chain_id} AND tx_hash = '{tx_hash}'")
        data = cursor.fetchone()
        if data:
            return jsonify({"error": "Transaction already exists"}), 400

        tx = evm_api.transaction.get_transaction(os.getenv("MORALIS_API_KEY_1"), {
            "chain": f"0x{chain_id:x}",
            "transaction_hash": tx_hash
        })

        from_address = tx["from_address"]
        to_address = tx["to_address"]
        block_number = tx["block_number"]
        timestamp = tx["block_timestamp"]
        timestamp = f"{timestamp[:10]} {timestamp[11:19]}"
        value = tx["value"]

        # Think that it is transfer money tx, so we need to also update addresses

        cursor.execute("SELECT chain_id FROM chains")
        chains = cursor.fetchall()

        native_dollar_balance = 0
        erc20_count = 0
        erc20_dollar_balance = 0
        nft_count = 0
        
        for chain in chains:
            _chain_id = chain["chain_id"]

            tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY_2"), {
                "chain": f"0x{_chain_id:x}",
                "address": from_address
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
                "address": from_address
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
            from_address,
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

            tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY_4"), {
                "chain": f"0x{_chain_id:x}",
                "address": to_address
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
                "address": to_address
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
            to_address,
            round(float(native_dollar_balance), 18),
            int(erc20_count),
            round(float(erc20_dollar_balance), 18),
            int(nft_count)
        ))

        block = evm_api.block.get_block(os.getenv("MORALIS_API_KEY_1"), {
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

            tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY_2"), {
                "chain": f"0x{_chain_id:x}",
                "address": miner
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
            INSERT IGNORE INTO blocks (chain_id, block_number, block_hash, parent_hash, miner, tx_count, timestamp)
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

        sql = f"""
            INSERT INTO transactions (chain_id, tx_hash, from_address, to_address, block_number, value, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (
            int(chain_id),
            tx_hash,
            from_address,
            to_address,
            int(block_number),
            float(value),
            timestamp
        ))

        return jsonify({"message": "Transaction added successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@transactions.route("/full/<int:chain_id>/<string:tx_hash>", methods=['POST'])
def full_add_transaction(chain_id, tx_hash):
    tx = evm_api.transaction.get_transaction(os.getenv("MORALIS_API_KEY_1"), {
        "chain": f"0x{chain_id:x}",
        "transaction_hash": tx_hash
    })

    block_number = tx["block_number"]

    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM chains WHERE chain_id = {chain_id}")
        chain = cursor.fetchone()
        if not chain:
            return jsonify({"error": "Chain not found"}), 404

        block = evm_api.block.get_block(os.getenv("MORALIS_API_KEY_1"), {
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

            tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY_4"), {
                "chain": f"0x{_chain_id:x}",
                "address": miner
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
            INSERT IGNORE INTO blocks (chain_id, block_number, block_hash, parent_hash, miner, tx_count, timestamp)
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

                tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY_2"), {
                    "chain": f"0x{_chain_id:x}",
                    "address": _address
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

                tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY_4"), {
                    "chain": f"0x{_chain_id:x}",
                    "address": _address
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
                INSERT IGNORE INTO transactions (chain_id, tx_hash, from_address, to_address, block_number, value, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(sql, (
                int(chain_id),
                tx_hash,
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