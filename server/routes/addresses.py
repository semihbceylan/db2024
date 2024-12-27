from flask import Blueprint, jsonify, request
from mysql.connector import Error

from utils.get_db_connection import get_db_connection

addresses = Blueprint('addresses', __name__)

@addresses.route("/<string:address>", methods=['GET'])
def get_address(address):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM addresses WHERE address = '{address}'")
        data = cursor.fetchone()
        if not data:
            return jsonify({"error": "Address not found"}), 404
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@addresses.route("/<string:address>", methods=['DELETE'])
def delete_address(address):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM addresses WHERE address = '{address}'")
        if cursor.rowcount == 0:
            return jsonify({"error": "Address not found"}), 404
        cursor.execute(f"SELECT block_number, chain_id FROM blocks WHERE miner = '{address}'")
        blocks_to_delete = cursor.fetchall()
        blocks_deleted = cursor.rowcount
        transactions_deleted = 0
        for block in blocks_to_delete:
            block_number = block["block_number"]
            chain_id = block["chain_id"]
            cursor.execute(f"DELETE FROM transactions WHERE chain_id = {chain_id} AND block_number = {block_number}") # in case of error we need to first delete the trasactions 
            transactions_deleted += cursor.rowcount
            cursor.execute(f"DELETE FROM blocks WHERE chain_id = {chain_id} AND block_number = {block_number}")
        cursor.execute(f"DELETE FROM nfts WHERE owner = '{address}'")
        nfts_deleted = cursor.rowcount
        return jsonify({
            "message": "Address and related data deleted successfully",
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