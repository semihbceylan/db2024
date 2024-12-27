from flask import Blueprint, jsonify, request
from mysql.connector import Error

from utils.get_db_connection import get_db_connection

chains = Blueprint('chains', __name__)

@chains.route("/", methods=['GET'])
def get_chains ():
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM chains")
        data = cursor.fetchall()
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@chains.route("/<int:chain_id>", methods=['DELETE'])
def delete_chain(chain_id):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM chains WHERE chain_id = {chain_id}")
        if cursor.rowcount == 0:
            return jsonify({"error": "Chain not found"}), 404
        cursor.execute(f"DELETE FROM blocks WHERE chain_id = {chain_id}")
        blocks_deleted = cursor.rowcount
        cursor.execute(f"DELETE FROM transactions WHERE chain_id = {chain_id}")
        transactions_deleted = cursor.rowcount
        cursor.execute(f"DELETE FROM nfts WHERE chain_id = {chain_id}")
        nfts_deleted = cursor.rowcount
        return jsonify({
            "message": "Chain and related data deleted successfully",
            "blocks_deleted": blocks_deleted,
            "transactions_deleted": transactions_deleted,
            "nfts_deleted": nfts_deleted
        }), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

# @chains.route("/", methods=["POST"])
# def add_chain():
#     """Add a new chain to the database."""
#     data = request.json
#     required_fields = ["chain_id", "chain_name", "native_currency", "total_supply"]

#     if not all(field in data for field in required_fields):
#         return jsonify({"error": "Missing required fields"}), 400

#     connection = get_db_connection()
#     if not connection:
#         return jsonify({"error": "Database connection failed"}), 500

#     try:
#         cursor = connection.cursor()
#         query = "INSERT INTO chains (chain_id, chain_name, native_currency, total_supply) VALUES (%s, %s, %s, %s)"
#         values = (data["chain_id"], data["chain_name"], data["native_currency"], data["total_supply"])
#         cursor.execute(query, values)
#         connection.commit()
#         return jsonify({"success": True, "message": "Chain added successfully"}), 201
#     except Error as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()

# @chains.route("/<int:chain_id>", methods=["PUT"])
# def edit_chain(chain_id):
#     """Edit a chain by its ID."""
#     data = request.json
#     required_fields = ["chain_name", "native_currency", "total_supply"]

#     if not all(field in data for field in required_fields):
#         return jsonify({"error": "Missing required fields"}), 400

#     connection = get_db_connection()
#     if not connection:
#         return jsonify({"error": "Database connection failed"}), 500

#     try:
#         cursor = connection.cursor()
#         query = "UPDATE chains SET chain_name = %s, native_currency = %s, total_supply = %s WHERE chain_id = %s"
#         values = (data["chain_name"], data["native_currency"], data["total_supply"], chain_id)
#         cursor.execute(query, values)
#         connection.commit()
#         return jsonify({"success": True, "message": "Chain updated successfully"}), 200
#     except Error as e:
#         return jsonify({"error": str(e)}), 500
#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()