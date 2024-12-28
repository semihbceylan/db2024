from dotenv import load_dotenv
import os

from moralis import evm_api
import mysql.connector

load_dotenv()

api_key = os.getenv("MORALIS_API_KEY")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

connection = mysql.connector.connect(**DB_CONFIG)
cursor = connection.cursor(dictionary=True)

def setup_db():
    cursor.execute("DROP TABLE IF EXISTS addresses")
    cursor.execute("DROP TABLE IF EXISTS blocks")
    cursor.execute("DROP TABLE IF EXISTS chains")
    cursor.execute("DROP TABLE IF EXISTS nfts")
    cursor.execute("DROP TABLE IF EXISTS transactions")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS addresses (
            address VARCHAR(42),
            native_balance FLOAT,
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

setup_db()