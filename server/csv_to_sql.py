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

df = pd.read_csv("./data/addresses.csv")
for _, row in df.iterrows():
    sql = f"""
        INSERT INTO addresses ({", ".join(df.columns)})
        VALUES ({", ".join(["%s"] * len(df.columns))})
    """

    cursor.execute(sql, (
        row['address'],
        round(float(row['native_dollar_balance']), 18),
        int(row['erc20_count']),
        round(float(row['erc20_dollar_balance']), 18), 
        int(row['nft_count'])
    ))

df = pd.read_csv("./data/blocks.csv")
for _, row in df.iterrows():
    sql = f"""
        INSERT INTO blocks ({", ".join(df.columns)})
        VALUES ({", ".join(["%s"] * len(df.columns))})
    """

    cursor.execute(sql, (
        int(row['chain_id']),
        int(row['block_number']),
        row['block_hash'],
        row['parent_hash'],
        row['miner'],
        int(row['tx_count']),
        row['timestamp']
    ))

df = pd.read_csv("./data/chains.csv")
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

df = pd.read_csv("./data/nfts.csv")
for _, row in df.iterrows():
    sql = f"""
        INSERT INTO nfts ({", ".join(df.columns)})
        VALUES ({", ".join(["%s"] * len(df.columns))})
    """
    cursor.execute(sql, (
        int(row['chain_id']),
        row['contract_address'],
        int(row['token_id']),
        row['owner'],
        row['contract_type'],
        row['name']
    ))

df = pd.read_csv("./data/transactions.csv")
for _, row in df.iterrows():
    sql = f"""
        INSERT INTO transactions ({", ".join(df.columns)})
        VALUES ({", ".join(["%s"] * len(df.columns))})
    """

    cursor.execute(sql, (
        int(row['chain_id']), 
        row['tx_hash'], 
        row['from_address'], 
        row['to_address'], 
        int(row['block_number']), 
        float(row['value']),
        row['timestamp']
    ))

connection.commit()