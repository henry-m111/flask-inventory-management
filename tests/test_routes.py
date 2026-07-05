import pytest
from unittest.mock import patch
import app as flask_app
import models


@pytest.fixture
def client():
    """Provide a test client and reset inventory before each test."""
    models.inventory.clear()
    models.next_id = 1
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as client:
        yield client


def test_get_inventory_empty(client):
    """GET /inventory should return an empty list when no items exist."""
    response = client.get("/inventory")
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_item(client):
    """POST /inventory should create a new item and return it with a 201 status."""
    response = client.post("/inventory", json={
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 4.99,
        "quantity": 20,
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Organic Almond Milk"
    assert data["id"] == 1

def test_get_single_item(client):
    """GET /inventory/<id> should return the correct item."""
    client.post("/inventory", json={
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 4.99,
        "quantity": 20,
    })
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Organic Almond Milk"


def test_get_single_item_not_found(client):
    """GET /inventory/<id> should return 404 for a non-existent item."""
    response = client.get("/inventory/999")
    assert response.status_code == 404

def test_update_item(client):
    """PATCH /inventory/<id> should update the item's fields."""
    client.post("/inventory", json={
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 4.99,
        "quantity": 20,
    })
    response = client.patch("/inventory/1", json={"price": 3.99, "quantity": 15})
    assert response.status_code == 200
    data = response.get_json()
    assert data["price"] == 3.99
    assert data["quantity"] == 15


def test_update_item_not_found(client):
    """PATCH /inventory/<id> should return 404 for a non-existent item."""
    response = client.patch("/inventory/999", json={"price": 1.00})
    assert response.status_code == 404


def test_delete_item(client):
    """DELETE /inventory/<id> should remove the item."""
    client.post("/inventory", json={
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 4.99,
        "quantity": 20,
    })
    response = client.delete("/inventory/1")
    assert response.status_code == 200

    get_response = client.get("/inventory/1")
    assert get_response.status_code == 404


def test_delete_item_not_found(client):
    """DELETE /inventory/<id> should return 404 for a non-existent item."""
    response = client.delete("/inventory/999")
    assert response.status_code == 404

def test_search_items_by_name(client):
    """GET /inventory/search should return items matching the name query."""
    client.post("/inventory", json={
        "name": "Organic Almond Milk",
        "brand": "Silk",
        "price": 4.99,
        "quantity": 20,
    })
    response = client.get("/inventory/search?name=almond")
    assert response.status_code == 200
    results = response.get_json()
    assert len(results) == 1
    assert results[0]["name"] == "Organic Almond Milk"


def test_search_items_missing_query(client):
    """GET /inventory/search without a name param should return a 400 error."""
    response = client.get("/inventory/search")
    assert response.status_code == 400

def test_fetch_and_add_item(client):
    """POST /inventory/fetch/<barcode> should fetch from OpenFoodFacts (mocked) and add to inventory."""
    fake_product = {
        "barcode": "3017620422003",
        "name": "Nutella",
        "brand": "Ferrero",
        "ingredients_text": "Sugar, palm oil, hazelnuts",
    }
    with patch("app.external_api.fetch_product_by_barcode", return_value=fake_product):
        response = client.post("/inventory/fetch/3017620422003")
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "Nutella"


def test_fetch_and_add_item_not_found(client):
    """POST /inventory/fetch/<barcode> should return 404 when product isn't found."""
    with patch("app.external_api.fetch_product_by_barcode", return_value=None):
        response = client.post("/inventory/fetch/0000000000000")
        assert response.status_code == 404