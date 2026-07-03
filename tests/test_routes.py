"""
Unit tests for the Flask API routes (CRUD operations).
Uses Flask's test client to simulate requests without running a live server.
"""

import pytest
import app as flask_app_module
import models


@pytest.fixture
def client():
    """Provides a Flask test client, and resets inventory data before each test."""
    flask_app_module.app.config["TESTING"] = True

    # Reset the in-memory inventory before every test so tests don't interfere
    models.inventory.clear()
    models.inventory.extend([
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
    ])
    models.next_id = 3

    with flask_app_module.app.test_client() as test_client:
        yield test_client


def test_get_all_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]["product_name"] == "Organic Almond Milk"


def test_get_single_item_success(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == 1
    assert data["brand"] == "Silk"


def test_get_single_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data


def test_create_item_success(client):
    new_item = {
        "product_name": "Peanut Butter",
        "brand": "Jif",
        "barcode": "0051500255516",
        "category": "Spreads",
        "quantity_in_stock": 20,
        "price": 4.29,
        "ingredients_text": "Roasted peanuts, sugar, salt.",
    }
    response = client.post("/inventory", json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    assert data["id"] == 3
    assert data["product_name"] == "Peanut Butter"

    # Confirm it actually landed in the inventory
    get_response = client.get("/inventory")
    assert len(get_response.get_json()) == 3


def test_create_item_missing_product_name(client):
    response = client.post("/inventory", json={"brand": "NoName"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_update_item_success(client):
    response = client.patch("/inventory/1", json={"price": 4.50, "quantity_in_stock": 40})
    assert response.status_code == 200
    data = response.get_json()
    assert data["price"] == 4.50
    assert data["quantity_in_stock"] == 40
    # Unchanged fields should remain the same
    assert data["product_name"] == "Organic Almond Milk"


def test_update_item_not_found(client):
    response = client.patch("/inventory/999", json={"price": 1.00})
    assert response.status_code == 404


def test_delete_item_success(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200

    # Confirm it's actually gone
    get_response = client.get("/inventory/1")
    assert get_response.status_code == 404


def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404