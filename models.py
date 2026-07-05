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