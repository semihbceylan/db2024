from flask import Flask, jsonify, request
from flask_cors import CORS

from utils.get_db_connection import get_db_connection
from mysql.connector import Error

from routes.transactions import transactions
from routes.addresses import addresses
from routes.blocks import blocks
from routes.chains import chains
from routes.nfts import nfts

app = Flask(__name__)
CORS(app)

app.register_blueprint(transactions, url_prefix='/transactions')
app.register_blueprint(addresses, url_prefix="/addresses")
app.register_blueprint(blocks, url_prefix='/blocks')
app.register_blueprint(chains, url_prefix="/chains")
app.register_blueprint(nfts, url_prefix="/nfts")

@app.route("/")
def home_route():
    return "<h1>DB2024 SERVER</h1>"

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)