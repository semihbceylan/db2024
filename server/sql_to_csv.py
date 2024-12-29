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

def query_to_csv(table_name):
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [desc[0] for desc in cursor.description]
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(f"./data/{table_name}.csv", index=False)

query_to_csv("addresses")
query_to_csv("blocks")
query_to_csv("chains")
query_to_csv("nfts")
query_to_csv("transactions")