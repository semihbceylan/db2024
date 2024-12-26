import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow access from all origins

load_dotenv()

# Database configuration
DB_CONFIG = {

    "host": "localhost",  # Change to your database host if it's remote
    "user": "root",
    "password": "yusa5444",
    "database": "dbsystems"

    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),

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


# --------------- BLOCKS ---------------
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

# Get a specific block
@app.route("/blocks/<int:chain_id>/<int:block_number>", methods=["GET"])
def get_block(chain_id, block_number):
    """Fetch a specific block by chain_id and block_number."""
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM blocks WHERE chain_id = %s AND block_number = %s"
        cursor.execute(query, (chain_id, block_number))
        block = cursor.fetchone()
        if not block:
            return jsonify({"error": "Block not found"}), 404
        return jsonify(block)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Create a new block
@app.route("/blocks", methods=["POST"])
def create_block():
    """Create a new block."""
    data = request.json
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = """
            INSERT INTO blocks (chain_id, block_number, transaction_count)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (data["chain_id"], data["block_number"], data["transaction_count"]))
        connection.commit()
        return jsonify({"message": "Block created successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Update transaction_count for a block
@app.route("/blocks/<int:chain_id>/<int:block_number>", methods=["PUT"])
def update_block(chain_id, block_number):
    """Update transaction_count for a block."""
    data = request.json
    if "transaction_count" not in data:
        return jsonify({"error": "transaction_count is required"}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = """
            UPDATE blocks SET transaction_count = %s
            WHERE chain_id = %s AND block_number = %s
        """
        cursor.execute(query, (data["transaction_count"], chain_id, block_number))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Block not found"}), 404
        return jsonify({"message": "Block updated successfully"})
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Delete a block
@app.route("/blocks/<int:chain_id>/<int:block_number>", methods=["DELETE"])
def delete_block(chain_id, block_number):
    """Delete a block."""
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = "DELETE FROM blocks WHERE chain_id = %s AND block_number = %s"
        cursor.execute(query, (chain_id, block_number))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Block not found"}), 404
        return jsonify({"message": "Block deleted successfully"})
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route("/addresses", methods=["GET"])
def get_addresses():
    """Fetch all addresses from the database."""
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM addresses")
        data = cursor.fetchall()
        return jsonify(data)
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route("/addresses", methods=["POST"])
def add_address():
    """Add a new address to the database."""
    data = request.json
    required_fields = ["address", "is_contract", "eth_balance", "erc20_count", "dollar_balance", "nft_count"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = """INSERT INTO addresses (address, is_contract, eth_balance, erc20_count, dollar_balance, nft_count)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (data["address"], data["is_contract"], data["eth_balance"], data["erc20_count"], data["dollar_balance"], data["nft_count"])
        cursor.execute(query, values)
        connection.commit()
        return jsonify({"success": True, "message": "Address added successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route("/addresses/<string:address>", methods=["DELETE"])
def delete_address(address):
    """Delete an address by its address value."""
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = "DELETE FROM addresses WHERE address = %s"
        cursor.execute(query, (address,))
        connection.commit()
        return jsonify({"success": True, "message": "Address deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@app.route("/addresses/<string:address>", methods=["PUT"])
def edit_address(address):
    """Edit an address by its address value."""
    data = request.json
    required_fields = ["is_contract", "eth_balance", "erc20_count", "dollar_balance", "nft_count"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor()
        query = """UPDATE addresses 
                   SET is_contract = %s, eth_balance = %s, erc20_count = %s, dollar_balance = %s, nft_count = %s
                   WHERE address = %s"""
        values = (data["is_contract"], data["eth_balance"], data["erc20_count"], data["dollar_balance"], data["nft_count"], address)
        cursor.execute(query, values)
        connection.commit()
        return jsonify({"success": True, "message": "Address updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


    # --------------- *** ---------------
            
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)


    