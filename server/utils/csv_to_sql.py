import mysql.connector
import pandas as pd

from dotenv import load_dotenv
import os

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

connection = mysql.connector.connect(**DB_CONFIG)
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS addresses")
cursor.execute("DROP TABLE IF EXISTS blocks")
cursor.execute("DROP TABLE IF EXISTS chains")
cursor.execute("DROP TABLE IF EXISTS nfts")
cursor.execute("DROP TABLE IF EXISTS transactions")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS addresses (
        address VARCHAR(42),
        is_contract TINYINT(1),
        eth_balance DECIMAL(30,18),
        erc20_count INT,
        dollar_balance DECIMAL(30,8),
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
        transaction_count INT,
        timestamp DATETIME,
        PRIMARY KEY (chain_id, block_number)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS chains (
        chain_id INT,
        chain_name VARCHAR(50),
        native_currency VARCHAR(10),
        explorer_url VARCHAR(255),
        rpc_url VARCHAR(255),
        PRIMARY KEY (chain_id)
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS nfts (
        address VARCHAR(42),
        token_id BIGINT,
        chain_id INT,
        owner VARCHAR(42),
        token_uri TEXT,
        contract_type VARCHAR(10),
        PRIMARY KEY (address, token_id)
    )           
""")


cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        tx_hash VARCHAR(66),
        from_address VARCHAR(42),
        to_address VARCHAR(42),
        block_number BIGINT,
        chain_id INT,
        timestamp DATETIME,
        value DECIMAL(30,18),
        PRIMARY KEY (tx_hash)
    )
""")

cursor.execute("DELETE FROM addresses")
cursor.execute("DELETE FROM blocks")
cursor.execute("DELETE FROM chains")
cursor.execute("DELETE FROM nfts")
cursor.execute("DELETE FROM transactions")

df = pd.read_csv("../data/addresses.csv")
for _, row in df.iterrows():
    sql = f"""
        INSERT INTO addresses ({", ".join(df.columns)})
        VALUES ({", ".join(["%s"] * len(df.columns))})
    """

    cursor.execute(sql, (
        row['address'],
        1 if row['is_contract'] else 0,
        round(float(row['eth_balance']), 18),
        int(row['erc20_count']),
        round(float(row['dollar_balance']), 8), 
        int(row['nft_count'])
    ))

df = pd.read_csv("../data/blocks.csv")
for _, row in df.iterrows():
    sql = f"""
        INSERT INTO blocks ({", ".join(df.columns)})
        VALUES ({", ".join(["%s"] * len(df.columns))})
    """

    cursor.execute(sql, (
        int(row['block_number']),
        int(row['chain_id']),
        row['block_hash'],
        row['parent_hash'],
        row['miner'],
        int(row['transaction_count']),
        row['timestamp']
    ))

df = pd.read_csv("../data/chains.csv")
for _, row in df.iterrows():
    sql = f"""
        INSERT INTO chains ({", ".join(df.columns)})
        VALUES ({", ".join(["%s"] * len(df.columns))})
    """

    cursor.execute(sql, (
        int(row['chain_id']),
        row['chain_name'],
        row['native_currency'],
        row['explorer_url'],
        row['rpc_url']
    ))

df = pd.read_csv("../data/nfts.csv")
for _, row in df.iterrows():
    sql = f"""
        INSERT INTO nfts ({", ".join(df.columns)})
        VALUES ({", ".join(["%s"] * len(df.columns))})
    """
    cursor.execute(sql, (
        row['address'],
        int(row['chain_id']),
        row['owner'],
        int(row['token_id']),
        row['token_uri'],
        row['contract_type']
    ))

df = pd.read_csv("../data/transactions.csv")
for _, row in df.iterrows():
    sql = f"""
        INSERT INTO transactions ({", ".join(df.columns)})
        VALUES ({", ".join(["%s"] * len(df.columns))})
    """

    cursor.execute(sql, (
        row['tx_hash'], 
        row['from_address'], 
        row['to_address'], 
        int(row['block_number']), 
        int(row['chain_id']), 
        row['timestamp'], 
        float(row['value'])
    ))

connection.commit()