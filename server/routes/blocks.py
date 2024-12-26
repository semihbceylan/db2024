from flask import Blueprint, jsonify, request
from mysql.connector import Error

from utils.get_db_connection import get_db_connection

blocks = Blueprint('blocks', __name__)

@blocks.route("/", methods=["GET"])
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
@blocks.route("/<int:chain_id>/<int:block_number>", methods=["GET"])
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
@blocks.route("/", methods=["POST"])
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
@blocks.route("/<int:chain_id>/<int:block_number>", methods=["PUT"])
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
@blocks.route("/<int:chain_id>/<int:block_number>", methods=["DELETE"])
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