# flask-inventory-management

A Flask REST API for managing retail inventory, with OpenFoodFacts integration
for real-time product data and a CLI frontend for interacting with the system.

Tech Stack

Python, Flask, Requests, Pytest

Installation & Setup

git clone https://github.com/henry-m111/flask-inventory-management.git
cd flask-inventory-management
python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Running the API

python3 app.py

Runs at http://127.0.0.1:5000.

Running the CLI

With the Flask server running in one terminal, open a second terminal:
source venv/bin/activate
python3 cli.py

Example: viewing inventory

Choose an option: 1

ID  Product                  Brand          Stock   Price
------------------------------------------------------------
1   Organic Almond Milk      Silk           50      3.99
2   Whole Wheat Bread        Nature's Own   30      2.49

Example: importing a product from OpenFoodFacts

Choose an option: 7
Enter barcode to import: 3017624010701
Set price for this item: 5.99
Set quantity in stock: 25
Item imported successfully with ID 3.

API Endpoints

MethodEndpointDescriptionGET/inventoryFetch all inventory itemsGET/inventory/<id>Fetch a single item by IDPOST/inventoryAdd a new inventory itemPATCH/inventory/<id>Update an item (partial update)DELETE/inventory/<id>Delete an itemGET/inventory/lookup/barcode/<barcode>Preview a product from OpenFoodFacts by barcodeGET/inventory/lookup/name/<name>Search OpenFoodFacts by product namePOST/inventory/import/barcode/<barcode>Fetch a product from OpenFoodFacts and add it to inventory

Running Tests

pytest -v

Author

Henry Muchiri — Software Engineering Student, Moringa School