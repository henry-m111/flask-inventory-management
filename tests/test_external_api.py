from unittest.mock import patch, Mock
import external_api


def test_fetch_product_by_barcode_success():
    """Should return a trimmed product dict when OpenFoodFacts finds the product."""
    fake_response_data = {
        "status": 1,
        "product": {
            "product_name": "Nutella",
            "brands": "Ferrero",
            "ingredients_text": "Sugar, palm oil, hazelnuts",
        },
    }

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = fake_response_data

    with patch("external_api.requests.get", return_value=mock_response):
        result = external_api.fetch_product_by_barcode("3017620422003")

    assert result is not None
    assert result["name"] == "Nutella"
    assert result["brand"] == "Ferrero"


def test_fetch_product_by_barcode_not_found():
    """Should return None when OpenFoodFacts reports status 0 (product not found)."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"status": 0}

    with patch("external_api.requests.get", return_value=mock_response):
        result = external_api.fetch_product_by_barcode("0000000000000")

    assert result is None


def test_fetch_product_by_barcode_bad_status_code():
    """Should return None when the HTTP request itself fails (e.g. 403, 500)."""
    mock_response = Mock()
    mock_response.status_code = 403

    with patch("external_api.requests.get", return_value=mock_response):
        result = external_api.fetch_product_by_barcode("3017620422003")

    assert result is None