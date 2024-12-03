from flask import Flask, jsonify, redirect, url_for, render_template_string
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

# Default route with links to all pages
@app.route('/')
def index():
    links = {
        "NFTs Data": url_for('get_nfts_data'),
        "Chains Data": url_for('get_chains_data'),
    }
    # HTML template with links to all pages
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>API Navigation</title>
    </head>
    <body>
        <h1>Welcome to the API</h1>
        <ul>
        {% for name, link in links.items() %}
            <li><a href="{{ link }}">{{ name }}</a></li>
        {% endfor %}
        </ul>
    </body>
    </html>
    """
    return render_template_string(html_template, links=links)

# Fetches data from EOAs
@app.route('/api/NFTs')
def get_nfts_data():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM nfts")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(data)

@app.route('/api/chains')
def get_chains_data():
    connection = get_db_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM chains")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    
    print("Data fetched:", data)  # Debugging line
    return jsonify(data)

# Handle 404 errors
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Page not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
