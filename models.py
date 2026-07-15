"""
In-memory data store for the Inventory Management System.
Simulates a database using a Python list, since this lab
doesn't require a real database.
"""

inventory = []
next_id = 1


def get_all_items():
    """Return a shallow copy of all items currently in inventory.

    Returning a copy prevents external callers from accidentally mutating the
    internal in-memory store.
    """
    return list(inventory)


def _coerce_price(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _coerce_quantity(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def add_item(data):
    """Add a new item to inventory and return it.

    Accepts a mapping with optional keys: name, brand, price, quantity.
    Coerces `price` to float and `quantity` to int when possible. Missing
    numeric fields default to 0.
    """
    global next_id
    if not isinstance(data, dict):
        raise TypeError("data must be a dict")

    price = _coerce_price(data.get("price"))
    quantity = _coerce_quantity(data.get("quantity"))

    item = {
        "id": next_id,
        "name": data.get("name"),
        "brand": data.get("brand"),
        "price": price if price is not None else 0.0,
        "quantity": quantity if quantity is not None else 0,
    }

    inventory.append(item)
    next_id += 1
    return item


def get_item_by_id(item_id):
    """Return a single item by its id (int), or None if not found."""
    try:
        search_id = int(item_id)
    except (TypeError, ValueError):
        return None

    for item in inventory:
        if item["id"] == search_id:
            return item
    return None


def update_item(item_id, data):
    """Update an existing item's allowed fields.

    Only `name`, `brand`, `price`, and `quantity` are accepted. Types are
    coerced where appropriate. Returns the updated item, or None if not found.
    """
    if not isinstance(data, dict):
        raise TypeError("data must be a dict")

    item = get_item_by_id(item_id)
    if item is None:
        return None

    if "name" in data:
        item["name"] = data.get("name")
    if "brand" in data:
        item["brand"] = data.get("brand")
    if "price" in data:
        price = _coerce_price(data.get("price"))
        if price is not None:
            item["price"] = price
    if "quantity" in data:
        quantity = _coerce_quantity(data.get("quantity"))
        if quantity is not None:
            item["quantity"] = quantity

    return item


def delete_item(item_id):
    """Remove an item from inventory. Returns True if deleted, False if not found."""
    item = get_item_by_id(item_id)
    if item is None:
        return False
    inventory.remove(item)
    return True


def search_items_by_name(query):
    """Return all items whose name contains the search query (case-insensitive).

    If `query` is falsy (None or empty) an empty list is returned.
    """
    if not query:
        return []
    q = str(query).lower()
    return [item for item in inventory if item.get("name") and q in item["name"].lower()]