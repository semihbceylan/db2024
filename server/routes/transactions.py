from flask import Blueprint, jsonify, request
from mysql.connector import Error

from utils.get_db_connection import get_db_connection

transactions = Blueprint('transactions', __name__)

@transactions.route("/<string:tx_hash>", methods=['GET'])
def get_transaction(tx_hash):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM transactions WHERE tx_hash = '{tx_hash}'")
        data = cursor.fetchone()
        if not data:
            return jsonify({"error": "Transaction not found"}), 404
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@transactions.route("/<string:tx_hash>", methods=['DELETE'])
def delete_transaction(tx_hash):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM transactions WHERE tx_hash = '{tx_hash}'")
        if cursor.rowcount == 0:
            return jsonify({"error": "Transaction not found"}), 404
        return jsonify({"message": "Transaction deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()