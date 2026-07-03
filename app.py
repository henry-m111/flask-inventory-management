"""
Flask REST API for the Inventory Management System.
Provides CRUD endpoints for managing inventory items.
"""
import external_api
from flask import Flask, jsonify, request
import models

app = Flask(__name__)


@app.route("/")
def index():
    """Simple health-check route."""
    return jsonify({"message": "Inventory Management API is running."})


@app.route("/inventory", methods=["GET"])
def get_inventory():
    """Fetch all inventory items."""
    return jsonify(models.get_all_items()), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_inventory_item(item_id):
    """Fetch a single inventory item by id."""
    item = models.get_item_by_id(item_id)
    if item is None:
        return jsonify({"error": f"Item with id {item_id} not found."}), 404
    return jsonify(item), 200


@app.route("/inventory", methods=["POST"])
def create_inventory_item():
    """Add a new inventory item."""
    data = request.get_json()

    if not data or "product_name" not in data:
        return jsonify({"error": "product_name is required."}), 400

    new_item = models.add_item(data)
    return jsonify(new_item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    """Update an existing inventory item (partial update)."""
    data = request.get_json()

    if not data:
        return jsonify({"error": "No update data provided."}), 400

    updated_item = models.update_item(item_id, data)
    if updated_item is None:
        return jsonify({"error": f"Item with id {item_id} not found."}), 404

    return jsonify(updated_item), 200


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    """Delete an inventory item by id."""
    deleted = models.delete_item(item_id)
    if not deleted:
        return jsonify({"error": f"Item with id {item_id} not found."}), 404

    return jsonify({"message": f"Item with id {item_id} deleted."}), 200



@app.route("/inventory/lookup/barcode/<barcode>", methods=["GET"])
def lookup_by_barcode(barcode):
    """Look up a product on OpenFoodFacts by barcode (does not save it)."""
    product = external_api.get_product_by_barcode(barcode)

    if product is None:
        return jsonify({"error": f"No product found for barcode {barcode}."}), 404

    return jsonify(product), 200


@app.route("/inventory/lookup/name/<name>", methods=["GET"])
def lookup_by_name(name):
    """Search OpenFoodFacts by product name (does not save it)."""
    results = external_api.search_product_by_name(name)

    if not results:
        return jsonify({"error": f"No products found matching '{name}'."}), 404

    return jsonify(results), 200


@app.route("/inventory/import/barcode/<barcode>", methods=["POST"])
def import_by_barcode(barcode):
    """
    Look up a product by barcode on OpenFoodFacts and add it directly
    to the inventory. Allows overriding/adding fields (like price,
    quantity_in_stock) via the request body.
    """
    product = external_api.get_product_by_barcode(barcode)

    if product is None:
        return jsonify({"error": f"No product found for barcode {barcode}."}), 404

    # Allow the client to add inventory-specific fields (price, stock)
    # that OpenFoodFacts doesn't provide.
    extra_data = request.get_json(silent=True) or {}
    product.update(extra_data)

    new_item = models.add_item(product)
    return jsonify(new_item), 201




if __name__ == "__main__":
    app.run(debug=True)