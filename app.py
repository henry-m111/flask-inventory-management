from flask import Flask, jsonify, request
import models

app = Flask(__name__)


@app.route("/")
def index():
    return "Inventory Management API is running."


@app.route("/inventory", methods=["GET"])
def get_inventory():
    """Fetch all inventory items."""
    return jsonify(models.get_all_items()), 200


@app.route("/inventory", methods=["POST"])
def create_item():
    """Add a new inventory item."""
    data = request.get_json()
    new_item = models.add_item(data)
    return jsonify(new_item), 201

@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    """Fetch a single inventory item by id."""
    item = models.get_item_by_id(item_id)
    if item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


if __name__ == "__main__":
    app.run(debug=True)