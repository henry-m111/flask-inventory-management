"""
CLI frontend for the Inventory Management System.
Communicates with the Flask API over HTTP using the requests library.
Run the Flask server (python3 app.py) in a separate terminal before using this.
"""

import requests

BASE_URL = "http://127.0.0.1:5000"


def print_menu():
    print("\n===== Inventory Management CLI =====")
    print("1. View all inventory items")
    print("2. View a single item by ID")
    print("3. Add a new inventory item (manual entry)")
    print("4. Update an item's price or stock")
    print("5. Delete an item")
    print("6. Find item on OpenFoodFacts (by barcode)")
    print("7. Import item from OpenFoodFacts (by barcode)")
    print("0. Exit")


def view_all_items():
    try:
        response = requests.get(f"{BASE_URL}/inventory")
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error: could not reach the API. {e}")
        return

    items = response.json()
    if not items:
        print("Inventory is empty.")
        return

    print(f"\n{'ID':<4}{'Product':<25}{'Brand':<15}{'Stock':<8}{'Price':<8}")
    print("-" * 60)
    for item in items:
        print(f"{item['id']:<4}{item['product_name'][:24]:<25}{item['brand'][:14]:<15}"
              f"{item['quantity_in_stock']:<8}{item['price']:<8}")


def view_single_item():
    item_id = input("Enter item ID: ").strip()
    if not item_id.isdigit():
        print("Please enter a valid numeric ID.")
        return

    try:
        response = requests.get(f"{BASE_URL}/inventory/{item_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error: could not reach the API. {e}")
        return

    if response.status_code == 404:
        print(f"No item found with ID {item_id}.")
        return

    item = response.json()
    print("\n--- Item Details ---")
    for key, value in item.items():
        print(f"{key}: {value}")


def add_item_manual():
    print("\nEnter new item details:")
    product_name = input("Product name: ").strip()
    brand = input("Brand: ").strip()
    barcode = input("Barcode: ").strip()
    category = input("Category: ").strip()

    quantity = input("Quantity in stock: ").strip()
    price = input("Price: ").strip()

    if not product_name:
        print("Product name is required. Cancelling.")
        return

    try:
        quantity_in_stock = int(quantity) if quantity else 0
        price_val = float(price) if price else 0.0
    except ValueError:
        print("Quantity must be a whole number and price must be a number. Cancelling.")
        return

    payload = {
        "product_name": product_name,
        "brand": brand,
        "barcode": barcode,
        "category": category,
        "quantity_in_stock": quantity_in_stock,
        "price": price_val,
        "ingredients_text": "",
    }

    try:
        response = requests.post(f"{BASE_URL}/inventory", json=payload)
    except requests.exceptions.RequestException as e:
        print(f"Error: could not reach the API. {e}")
        return

    if response.status_code == 201:
        print(f"Item added successfully with ID {response.json()['id']}.")
    else:
        print(f"Failed to add item: {response.json()}")


def update_item():
    item_id = input("Enter item ID to update: ").strip()
    if not item_id.isdigit():
        print("Please enter a valid numeric ID.")
        return

    print("Leave a field blank to keep it unchanged.")
    price = input("New price: ").strip()
    quantity = input("New quantity in stock: ").strip()

    payload = {}
    try:
        if price:
            payload["price"] = float(price)
        if quantity:
            payload["quantity_in_stock"] = int(quantity)
    except ValueError:
        print("Price must be a number and quantity must be a whole number. Cancelling.")
        return

    if not payload:
        print("No changes provided.")
        return

    try:
        response = requests.patch(f"{BASE_URL}/inventory/{item_id}", json=payload)
    except requests.exceptions.RequestException as e:
        print(f"Error: could not reach the API. {e}")
        return

    if response.status_code == 200:
        print("Item updated successfully.")
    elif response.status_code == 404:
        print(f"No item found with ID {item_id}.")
    else:
        print(f"Failed to update item: {response.json()}")


def delete_item():
    item_id = input("Enter item ID to delete: ").strip()
    if not item_id.isdigit():
        print("Please enter a valid numeric ID.")
        return

    confirm = input(f"Are you sure you want to delete item {item_id}? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/inventory/{item_id}")
    except requests.exceptions.RequestException as e:
        print(f"Error: could not reach the API. {e}")
        return

    if response.status_code == 200:
        print("Item deleted successfully.")
    elif response.status_code == 404:
        print(f"No item found with ID {item_id}.")
    else:
        print(f"Failed to delete item: {response.json()}")


def find_item_on_api():
    barcode = input("Enter barcode to look up: ").strip()
    if not barcode:
        print("Barcode cannot be empty.")
        return

    try:
        response = requests.get(f"{BASE_URL}/inventory/lookup/barcode/{barcode}")
    except requests.exceptions.RequestException as e:
        print(f"Error: could not reach the API. {e}")
        return

    if response.status_code == 404:
        print(f"No product found for barcode {barcode}.")
        return

    product = response.json()
    print("\n--- Product Found on OpenFoodFacts ---")
    for key, value in product.items():
        print(f"{key}: {value}")


def import_item_from_api():
    barcode = input("Enter barcode to import: ").strip()
    if not barcode:
        print("Barcode cannot be empty.")
        return

    price = input("Set price for this item: ").strip()
    quantity = input("Set quantity in stock: ").strip()

    payload = {}
    try:
        if price:
            payload["price"] = float(price)
        if quantity:
            payload["quantity_in_stock"] = int(quantity)
    except ValueError:
        print("Price must be a number and quantity must be a whole number. Cancelling.")
        return

    try:
        response = requests.post(f"{BASE_URL}/inventory/import/barcode/{barcode}", json=payload)
    except requests.exceptions.RequestException as e:
        print(f"Error: could not reach the API. {e}")
        return

    if response.status_code == 201:
        print(f"Item imported successfully with ID {response.json()['id']}.")
    elif response.status_code == 404:
        print(f"No product found for barcode {barcode}.")
    else:
        print(f"Failed to import item: {response.json()}")


def main():
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            view_all_items()
        elif choice == "2":
            view_single_item()
        elif choice == "3":
            add_item_manual()
        elif choice == "4":
            update_item()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            find_item_on_api()
        elif choice == "7":
            import_item_from_api()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()