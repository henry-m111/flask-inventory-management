"""
In-memory data store for the Inventory Management System.
Simulates a database using a Python list of dictionaries.
Each item is shaped to resemble OpenFoodFacts product data,
plus inventory-specific fields (quantity_in_stock, price).
"""

# Simulated database (in-memory list)
inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "barcode": "0025293001156",
        "category": "Beverages",
        "quantity_in_stock": 50,
        "price": 3.99,
        "ingredients_text": "Filtered water, almonds, cane sugar, sea salt, vitamins.",
    },
    {
        "id": 2,
        "product_name": "Whole Wheat Bread",
        "brand": "Nature's Own",
        "barcode": "0072250010013",
        "category": "Bakery",
        "quantity_in_stock": 30,
        "price": 2.49,
        "ingredients_text": "Whole wheat flour, water, yeast, honey, salt.",
    },
]

# Tracks the next available ID for new items
next_id = 3


def get_all_items():
    """Return every item in the inventory."""
    return inventory


def get_item_by_id(item_id):
    """Return a single item by its id, or None if not found."""
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None


def add_item(data):
    """
    Add a new item to the inventory.
    'data' is a dict containing the new item's fields (no id needed).
    Returns the newly created item (with its assigned id).
    """
    global next_id
    new_item = {
        "id": next_id,
        "product_name": data.get("product_name", ""),
        "brand": data.get("brand", ""),
        "barcode": data.get("barcode", ""),
        "category": data.get("category", ""),
        "quantity_in_stock": data.get("quantity_in_stock", 0),
        "price": data.get("price", 0.0),
        "ingredients_text": data.get("ingredients_text", ""),
    }
    inventory.append(new_item)
    next_id += 1
    return new_item


def update_item(item_id, data):
    """
    Update an existing item with the given fields (partial update / PATCH).
    Returns the updated item, or None if not found.
    """
    item = get_item_by_id(item_id)
    if item is None:
        return None
    item.update(data)
    return item


def delete_item(item_id):
    """
    Remove an item from the inventory by id.
    Returns True if deleted, False if not found.
    """
    item = get_item_by_id(item_id)
    if item is None:
        return False
    inventory.remove(item)
    return True