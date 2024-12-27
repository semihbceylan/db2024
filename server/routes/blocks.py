from flask import Blueprint, jsonify, request
from mysql.connector import Error

from utils.get_db_connection import get_db_connection

blocks = Blueprint('blocks', __name__)

@blocks.route("/<int:chain_id>/<int:block_number>", methods=['GET'])
def get_block(chain_id, block_number):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM blocks WHERE chain_id = {chain_id} AND block_number = {block_number}")
        data = cursor.fetchone()
        if not data:
            return jsonify({"error": "Block not found"}), 404
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@blocks.route("/<int:chain_id>/<int:block_number>", methods=['DELETE'])
def delete_block(chain_id, block_number):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM blocks WHERE chain_id = {chain_id} AND block_number = {block_number}")
        if cursor.rowcount == 0:
            return jsonify({"error": "Block not found"}), 404
        cursor.execute(f"DELETE FROM transactions WHERE chain_id = {chain_id} AND block_number = {block_number}")
        transactions_deleted = cursor.rowcount
        return jsonify({
            "message": "BLock and related data deleted successfully",
            "transactions_deleted": transactions_deleted,
        }), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

# # Create a new block
# @blocks.route("/", methods=["POST"])
# def create_block():
#     """Create a new block."""
#     data = request.json
#     connection = get_db_connection()
#     if not connection:
#         return jsonify({"error": "Database connection failed"}), 500

#     try:
#         cursor = connection.cursor()
#         query = """
#             INSERT INTO blocks (chain_id, block_number, transaction_count)
#             VALUES (%s, %s, %s)
#         """
#         cursor.execute(query, (data["chain_id"], data["block_number"], data["transaction_count"]))
#         connection.commit()
#         return jsonify({"message": "Block created successfully"}), 201
#     except Error as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()