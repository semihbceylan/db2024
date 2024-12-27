from flask import Blueprint, jsonify, request
from mysql.connector import Error

from utils.get_db_connection import get_db_connection

nfts = Blueprint('nfts', __name__)

@nfts.route("/", methods=['GET'])
def get_nfts ():
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM nfts")
        data = cursor.fetchall()
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@nfts.route("/<string:address>", methods=['GET'])
def get_nft_contract(address):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM nfts WHERE address = '{address}'")
        data = cursor.fetchall()
        if not data:
            return jsonify({"error": "NFT contract not found"}), 404
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@nfts.route("/<string:address>/<int:token_id>", methods=['GET'])
def get_nft(address, token_id):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM nfts WHERE address = '{address}' AND token_id = {token_id}")
        data = cursor.fetchone()
        if not data:
            return jsonify({"error": "NFT not found"}), 404
        return jsonify(data), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@nfts.route("/<string:address>", methods=['DELETE'])
def delete_nft_contract(address):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM nfts WHERE address = '{address}'")
        nfts_deleted = cursor.rowcount
        if nfts_deleted == 0:
            return jsonify({"error": "NFT contract not found"}), 404
        return jsonify({
            "message": "NFT contract deleted",
            "nfts_deleted": nfts_deleted
        }), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()

@nfts.route("/<string:address>/<int:token_id>", methods=['DELETE'])
def delete_nft(address, token_id):
    connection = get_db_connection()

    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"DELETE FROM nfts WHERE address = '{address}' AND token_id = {token_id}")
        if cursor.rowcount == 0:
            return jsonify({"error": "NFT not found"}), 404
        return jsonify({"message": "NFT deleted"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if connection.is_connected():
            connection.commit()
            cursor.close()
            connection.close()