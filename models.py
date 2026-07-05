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