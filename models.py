"""
In-memory data store for the Inventory Management System.
Simulates a database using a Python list, since this lab
doesn't require a real database.
"""

inventory = []
next_id = 1


def get_all_items():
    """Return all items currently in inventory."""
    return inventory


def add_item(data):
    """Add a new item to inventory and return it."""
    global next_id
    item = {
        "id": next_id,
        "name": data.get("name"),
        "brand": data.get("brand"),
        "price": data.get("price"),
        "quantity": data.get("quantity"),
    }
    inventory.append(item)
    next_id += 1
    return item


def get_item_by_id(item_id):
    """Return a single item by its id, or None if not found."""
    for item in inventory:
        if item["id"] == item_id:
            return item
    return None

def update_item(item_id, data):
    """Update an existing item's fields. Returns the updated item, or None if not found."""
    item = get_item_by_id(item_id)
    if item is None:
        return None
    if "name" in data:
        item["name"] = data["name"]
    if "brand" in data:
        item["brand"] = data["brand"]
    if "price" in data:
        item["price"] = data["price"]
    if "quantity" in data:
        item["quantity"] = data["quantity"]
    return item

def delete_item(item_id):
    """Remove an item from inventory. Returns True if deleted, False if not found."""
    item = get_item_by_id(item_id)
    if item is None:
        return False
    inventory.remove(item)
    return True