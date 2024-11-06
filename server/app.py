# server/app.py
from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB")
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

# Fetches data from EOAs
@app.route('/api/EOAs')
def get_eoas_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM eoas")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(data)

@app.route('/api/chains')
def get_chains_data():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM chains")
        data = cursor.fetchall()
        cursor.close()
        connection.close()
        
        print("Data fetched:", data)  # Debugging line
        return jsonify(data)

# Add your routes for your tables here

if __name__ == '__main__':
    app.run(debug=True)
