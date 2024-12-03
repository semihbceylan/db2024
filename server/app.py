from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow access from all origins

# Database configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),  # Default to localhost if not set
    "user": os.getenv("DB_USER", "root"),      # Default to root if not set
    "password": os.getenv("DB_PASSWORD", ""),  # Default to empty if not set
    "database": os.getenv("DB_NAME", "test")   # Default to "test" if not set
}

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# API Endpoints

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Welcome to the Flask API!"})

@app.route("/chains", methods=["GET"])
def get_chains():
    """Fetch all chains from the database."""
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM chains")
        data = cursor.fetchall()
        return jsonify(data)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/chains", methods=["POST"])
def add_chain():
    """Add a new chain to the database."""
    data = request.json
    required_fields = ["chain_id", "chain_name", "native_currency", "total_supply"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = "INSERT INTO chains (chain_id, chain_name, native_currency, total_supply) VALUES (%s, %s, %s, %s)"
        values = (data["chain_id"], data["chain_name"], data["native_currency"], data["total_supply"])
        cursor.execute(query, values)
        connection.commit()
        return jsonify({"success": True, "message": "Chain added successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/chains/<int:chain_id>", methods=["DELETE"])
def delete_chain(chain_id):
    """Delete a chain by its ID."""
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = "DELETE FROM chains WHERE chain_id = %s"
        cursor.execute(query, (chain_id,))
        connection.commit()
        return jsonify({"success": True, "message": "Chain deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/chains/<int:chain_id>", methods=["PUT"])
def edit_chain(chain_id):
    """Edit a chain by its ID."""
    data = request.json
    required_fields = ["chain_name", "native_currency", "total_supply"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = "UPDATE chains SET chain_name = %s, native_currency = %s, total_supply = %s WHERE chain_id = %s"
        values = (data["chain_name"], data["native_currency"], data["total_supply"], chain_id)
        cursor.execute(query, values)
        connection.commit()
        return jsonify({"success": True, "message": "Chain updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/blocks", methods=["GET"])
def blocks():
    """Fetch all blocks from the database."""
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM blocks")
        data = cursor.fetchall()
        return jsonify(data)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/blocks", methods=["POST"])
def add_block():
    """Add a new block to the database."""
    data = request.json
    required_fields = ["block_number", "chain_id", "block_hash", "parent_hash", "miner", "transaction_count", "timestamp"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = "INSERT INTO blocks (block_number, chain_id, block_hash, parent_hash, miner, transaction_count, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (data[block_number], data[chain_id], data[block_hash], data[parent_hash], data[miner], data[transaction_count], data[timestam])
        cursor.execute(query, values)
        connection.commit()
        return jsonify({"success": True, "message": "Chain added successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/blocks/<int:chain_id>", methods=["DELETE"])
def delete_block(chain_id):
    """Delete a block by its chain_id."""
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = "DELETE FROM blocks WHERE chain_id = %s"
        cursor.execute(query, (chain_id,))
        connection.commit()
        return jsonify({"success": True, "message": "Block with specified chain ID deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/blocks/<int:chain_id>", methods=["PUT"])
def edit_block(chain_id):
    """Edit a block by its chainId."""
    data = request.json
    required_fields = ["block_hash", "parent_hash", "miner", "transaction_count", "timestamp"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = "UPDATE blocks SET block_hash = %s, parant_hash = %s, miner = %s, transaction_count = %s, timestamp = %s WHERE chain_id = %s"
        values = (data["chain_name"], data["native_currency"], data["total_supply"], chain_id)
        cursor.execute(query, values)
        connection.commit()
        return jsonify({"success": True, "message": "Chain updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
