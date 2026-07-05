# Flask Inventory Management API

A REST API built with Flask for managing retail inventory, with integration into the OpenFoodFacts API to auto-populate product details by barcode. Includes a CLI tool for interacting with the API without a frontend.

Built as a summative lab project for Moringa School's Software Engineering program.

## Features

- Full CRUD REST API for inventory items (Create, Read, Update, Delete)
- Search inventory by name
- Fetch real product data from OpenFoodFacts by barcode and add it directly to inventory
- CLI tool for viewing, adding, updating, deleting, and fetching items
- In-memory data storage (a Python list simulating a database, per lab requirements)
- Full pytest test suite with mocked external API calls

## Tech Stack

- Python 3
- Flask
- requests (for OpenFoodFacts integration)
- pytest + unittest.mock (for testing)

## Setup & Installation

1. Clone the repository:
```bash
   git clone https://github.com/henry-m111/flask-inventory-management.git
   cd flask-inventory-management
```

2. Create and activate a virtual environment:
```bash
   python3 -m venv venv
   source venv/bin/activate
```

3. Install dependencies:
```bash
   pip install -r requirements.txt --break-system-packages
```

4. Run the Flask server:
```bash
   python app.py
```
   The API will be running at `http://127.0.0.1:5000`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|--------------|
| GET | `/inventory` | Get all inventory items |
| GET | `/inventory/<id>` | Get a single item by id |
| POST | `/inventory` | Create a new item |
| PATCH | `/inventory/<id>` | Update an item's fields |
| DELETE | `/inventory/<id>` | Delete an item |
| GET | `/inventory/search?name=` | Search items by name |
| POST | `/inventory/fetch/<barcode>` | Fetch a product from OpenFoodFacts by barcode and add it to inventory |

### Example: Create an item
```bash
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"name": "Organic Almond Milk", "brand": "Silk", "price": 4.99, "quantity": 20}'
```

### Example: Fetch a product from OpenFoodFacts
```bash
curl -X POST http://127.0.0.1:5000/inventory/fetch/3017620422003
```

## CLI Usage

With the Flask server running in one terminal, run the CLI in another:

```bash
python cli.py
```

Menu options:
1. View all items
2. Add new item
3. Update item
4. Delete item
5. Find item on API (by barcode)
6. Exit

## Running Tests

```bash
pytest -v
```

This runs the full test suite (20 tests) covering:
- All API routes (`tests/test_routes.py`)
- The OpenFoodFacts integration, with mocked HTTP calls (`tests/test_external_api.py`)
- The CLI functions, with mocked API calls and user input (`tests/test_cli.py`)

## Project Structure

flask-inventory-management/
├── app.py               # Flask app and route definitions
├── models.py             # In-memory inventory storage + helper functions
├── external_api.py       # OpenFoodFacts integration
├── cli.py                 # CLI frontend
├── requirements.txt
├── tests/
│   ├── test_routes.py
│   ├── test_external_api.py
│   └── test_cli.py
└── README.md

## Notes

- Inventory is stored in memory (a Python list), as required by the lab — this means data resets every time the Flask server restarts. In a production system this would be replaced with a real database.
- Fields like `price` and `quantity` are not available from OpenFoodFacts, so they come back as `null` when fetching a new product this way — they can be filled in afterward via the PATCH endpoint.
