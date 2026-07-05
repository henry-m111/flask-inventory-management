from flask import Flask, jsonify
import models

app = Flask(__name__)


@app.route("/")
def index():
    return "Inventory Management API is running."


@app.route("/inventory", methods=["GET"])
def get_inventory():
    """Fetch all inventory items."""
    return jsonify(models.get_all_items()), 200


if __name__ == "__main__":
    app.run(debug=True)