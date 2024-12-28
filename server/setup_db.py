from dotenv import load_dotenv
import os

from moralis import evm_api
import mysql.connector
import pandas as pd

load_dotenv()

api_key = os.getenv("MORALIS_API_KEY")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "charset": "utf8mb4"
}

connection = mysql.connector.connect(**DB_CONFIG)
cursor = connection.cursor(dictionary=True)

def setup_db(cursor):
    cursor.execute("DROP TABLE IF EXISTS addresses")
    cursor.execute("DROP TABLE IF EXISTS blocks")
    cursor.execute("DROP TABLE IF EXISTS chains")
    cursor.execute("DROP TABLE IF EXISTS nfts")
    cursor.execute("DROP TABLE IF EXISTS transactions")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS addresses (
            address VARCHAR(42),
            native_dollar_balance FLOAT,
            erc20_count INT,
            erc20_dollar_balance FLOAT,
            nft_count INT,
            PRIMARY KEY (address)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocks (
            chain_id INT,
            block_number INT,
            block_hash VARCHAR(66),
            parent_hash VARCHAR(66),
            miner VARCHAR(42),
            tx_count INT,
            timestamp DATETIME,
            PRIMARY KEY (chain_id, block_number)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chains (
            chain_id INT,
            chain_name VARCHAR(50),
            native_currency VARCHAR(50),
            explorer_url VARCHAR(255),
            rpc_url VARCHAR(255),
            PRIMARY KEY (chain_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nfts (
            chain_id INT,
            contract_address VARCHAR(42),
            token_id INT,
            owner VARCHAR(42),
            contract_type VARCHAR(10),
            name VARCHAR(255),
            PRIMARY KEY (chain_id, contract_address, token_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            chain_id INT,
            tx_hash VARCHAR(66),
            from_address VARCHAR(42),
            to_address VARCHAR(42),
            block_number INT,
            value FLOAT,
            timestamp DATETIME,
            PRIMARY KEY (chain_id, tx_hash)
        )
    """)

    cursor.execute("""
        INSERT INTO chains (chain_id, chain_name, native_currency, explorer_url, rpc_url)
        VALUES (1, "Ethereum Mainnet", "ETH", "https://etherscan.io", "https://cloudflare-eth.com")
    """)

    cursor.execute("""
        INSERT INTO chains (chain_id, chain_name, native_currency, explorer_url, rpc_url)
        VALUES (10, "OP Mainnet", "ETH", "https://optimistic.etherscan.io", "https://mainnet.optimism.io")
    """)

    cursor.execute("""
        INSERT INTO chains (chain_id, chain_name, native_currency, explorer_url, rpc_url)
        VALUES (137, "Polygon Mainnet", "MATIC", "https://polygonscan.com", "https://polygon-rpc.com/")
    """)

    cursor.execute("""
        INSERT INTO chains (chain_id, chain_name, native_currency, explorer_url, rpc_url)
        VALUES (8453, "Base", "ETH", "https://basescan.org", "https://mainnet.base.org/")
    """)

    connection.commit()

def fetch(chain_id, block_number, cursor):
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

            tokens = (evm_api.wallets.get_wallet_token_balances_price(os.getenv("MORALIS_API_KEY_5"), {
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

    connection.commit()

def fetch_nfts(cursor):
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

    connection.commit()

def query_to_csv(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]  # Sütun adlarını al
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(f"./data/{table_name}.csv", index=False)

# setup_db(cursor)

# fetch(1, 2068621, cursor)
# fetch(8453, 2068625, cursor)

# fetch_nfts(cursor)

query_to_csv("addresses")
query_to_csv("blocks")
query_to_csv("chains")
query_to_csv("nfts")
query_to_csv("transactions")