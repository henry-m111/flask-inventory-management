"""
Unit tests for the OpenFoodFacts external API integration.
Uses unittest.mock to simulate API responses without making real network calls.
"""

from unittest.mock import patch, MagicMock
import external_api


def test_get_product_by_barcode_success():
    """Should return a clean product dict when OpenFoodFacts finds the barcode."""
    mock_response_data = {
        "status": 1,
        "product": {
            "product_name": "Nutella",
            "brands": "Ferrero",
            "categories": "Spreads, Chocolate spreads",
            "ingredients_text": "Sugar, palm oil, hazelnuts.",
        },
    }

    with patch("external_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = external_api.get_product_by_barcode("3017624010701")

        assert result is not None
        assert result["product_name"] == "Nutella"
        assert result["brand"] == "Ferrero"
        assert result["barcode"] == "3017624010701"
        assert result["category"] == "Spreads"


def test_get_product_by_barcode_not_found():
    """Should return None when OpenFoodFacts has no data for the barcode (status 0)."""
    mock_response_data = {"status": 0}

    with patch("external_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = external_api.get_product_by_barcode("0000000000000")

        assert result is None


def test_get_product_by_barcode_network_error():
    """Should return None gracefully if the API call raises a network error."""
    with patch("external_api.requests.get") as mock_get:
        mock_get.side_effect = external_api.requests.exceptions.ConnectionError("No internet")

        result = external_api.get_product_by_barcode("3017624010701")

        assert result is None


def test_search_product_by_name_success():
    """Should return a list of simplified product dicts on a successful search."""
    mock_response_data = {
        "products": [
            {
                "product_name": "Almond Milk",
                "brands": "Silk",
                "code": "0025293001156",
                "categories": "Beverages, Plant-based drinks",
                "ingredients_text": "Water, almonds.",
            }
        ]
    }

    with patch("external_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        results = external_api.search_product_by_name("almond milk")

        assert len(results) == 1
        assert results[0]["product_name"] == "Almond Milk"
        assert results[0]["barcode"] == "0025293001156"


def test_search_product_by_name_no_results():
    """Should return an empty list when no products match."""
    mock_response_data = {"products": []}

    with patch("external_api.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = mock_response_data
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        results = external_api.search_product_by_name("nonexistentproduct123")

        assert results == []