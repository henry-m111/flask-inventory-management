# Flask Inventory Management API

Summative lab project for Moringa School. A small Flask API for managing inventory, with a CLI to interact with it and integration with the OpenFoodFacts API.

## What it does

- CRUD for inventory items (create, read, update, delete)
- Search items by name
- Fetch product info from OpenFoodFacts using a barcode and add it to inventory
- CLI to do all of the above without needing curl or Postman
- Data is stored in a Python list (no real database), so it resets when the server restarts
- pytest tests for the routes, the external API calls, and the CLI (mocked, so no real network calls in tests)

## Setup

```bash
git clone https://github.com/henry-m111/flask-inventory-management.git
cd flask-inventory-management
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt --break-system-packages
python app.py
```

Server runs at `http://127.0.0.1:5000`.

## Routes

- `GET /inventory` - all items
- `GET /inventory/<id>` - one item
- `POST /inventory` - add item
- `PATCH /inventory/<id>` - update item
- `DELETE /inventory/<id>` - delete item
- `GET /inventory/search?name=` - search by name
- `POST /inventory/fetch/<barcode>` - fetch from OpenFoodFacts and add to inventory

## CLI

```bash
python cli.py
```

Lets you view, add, update, delete items, and fetch a product by barcode.

## Tests

```bash
pytest -v
```