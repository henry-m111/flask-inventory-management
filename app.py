from flask import Flask, jsonify, request
import models
import external_api

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

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item_route(item_id):
    """Update fields on an existing inventory item."""
    data = request.get_json()
    updated_item = models.update_item(item_id, data)
    if updated_item is None:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(updated_item), 200

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item_route(item_id):
    """Delete an inventory item by id."""
    deleted = models.delete_item(item_id)
    if not deleted:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": "Item deleted"}), 200

@app.route("/inventory/fetch/<barcode>", methods=["POST"])
def fetch_and_add_item(barcode):
    """Fetch product details from OpenFoodFacts and add to inventory."""
    product_data = external_api.fetch_product_by_barcode(barcode)
    if product_data is None:
        return jsonify({"error": "Product not found in OpenFoodFacts"}), 404
    new_item = models.add_item(product_data)
    return jsonify(new_item), 201

@app.route("/inventory/search", methods=["GET"])
def search_items():
    """Search inventory items by name using a query parameter."""
    query = request.args.get("name", "")
    if not query:
        return jsonify({"error": "Please provide a 'name' query parameter"}), 400
    results = models.search_items_by_name(query)
    return jsonify(results), 200

if __name__ == "__main__":
    app.run(debug=True)