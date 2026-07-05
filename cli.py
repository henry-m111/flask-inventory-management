import requests

API_URL = "http://127.0.0.1:5000/inventory"


def view_items():
    """Fetch and display all inventory items."""
    try:
        response = requests.get(API_URL)
        items = response.json()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API. Is the server running?")
        return

    if not items:
        print("No items in inventory.")
        return
    for item in items:
        print(f"[{item['id']}] {item['name']} - {item['brand']} - ${item['price']} - qty: {item['quantity']}")

def add_item():
    """Prompt user for item details and add it via the API."""
    name = input("Item name: ")
    brand = input("Brand: ")
    price = input("Price: ")
    quantity = input("Quantity: ")

    data = {
        "name": name,
        "brand": brand,
        "price": float(price),
        "quantity": int(quantity),
    }

    response = requests.post(API_URL, json=data)
    if response.status_code == 201:
        print("Item added successfully:")
        print(response.json())
    else:
        print("Failed to add item.")

def update_item():
    """Prompt user for an item id and new values, then update via the API."""
    item_id = input("Item id to update: ")
    print("Leave a field blank to keep it unchanged.")
    name = input("New name: ")
    brand = input("New brand: ")
    price = input("New price: ")
    quantity = input("New quantity: ")

    data = {}
    if name:
        data["name"] = name
    if brand:
        data["brand"] = brand
    if price:
        data["price"] = float(price)
    if quantity:
        data["quantity"] = int(quantity)

    response = requests.patch(f"{API_URL}/{item_id}", json=data)
    if response.status_code == 200:
        print("Item updated successfully:")
        print(response.json())
    else:
        print("Failed to update item:", response.json())


def delete_item():
    """Prompt user for an item id and delete it via the API."""
    item_id = input("Item id to delete: ")
    response = requests.delete(f"{API_URL}/{item_id}")
    if response.status_code == 200:
        print("Item deleted successfully.")
    else:
        print("Failed to delete item:", response.json())

def main():
    while True:
        print("\n--- Inventory Management CLI ---")
        print("1. View all items")
        print("2. Add new item")
        print("3. Update item")
        print("4. Delete item")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            view_items()
        elif choice == "2":
            add_item()
        elif choice == "3":
            update_item()
        elif choice == "4":
            delete_item()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()