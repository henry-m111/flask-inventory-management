"""
Integration with the OpenFoodFacts API.
Provides functions to look up product data by barcode or by product name,
so it can be used to enrich items in our inventory.
"""

import requests

BASE_URL = "https://world.openfoodfacts.org/api/v2/product"
SEARCH_URL = "https://world.openfoodfacts.org/cgi/search.pl"

# OpenFoodFacts asks all apps to identify themselves with a custom User-Agent
HEADERS = {
    "User-Agent": "InventoryManagementApp - Moringa Lab - Version 1.0"
}


def get_product_by_barcode(barcode):
    """
    Fetch product details from OpenFoodFacts using a barcode.
    Returns a dict with product info, or None if not found / on error.
    """
    url = f"{BASE_URL}/{barcode}.json"

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error contacting OpenFoodFacts API: {e}")
        return None

    data = response.json()

    if data.get("status") != 1:
        # status 0 means the barcode wasn't found in the database
        return None

    product = data.get("product", {})

    return {
        "product_name": product.get("product_name", ""),
        "brand": product.get("brands", ""),
        "barcode": barcode,
        "category": product.get("categories", "").split(",")[0] if product.get("categories") else "",
        "ingredients_text": product.get("ingredients_text", ""),
    }


def search_product_by_name(name):
    """
    Search OpenFoodFacts for products matching a given name.
    Returns a list of simplified product dicts (may be empty).
    """
    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 5,
    }

    try:
        response = requests.get(SEARCH_URL, headers=HEADERS, params=params, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error contacting OpenFoodFacts API: {e}")
        return []

    data = response.json()
    products = data.get("products", [])

    results = []
    for product in products:
        results.append({
            "product_name": product.get("product_name", ""),
            "brand": product.get("brands", ""),
            "barcode": product.get("code", ""),
            "category": product.get("categories", "").split(",")[0] if product.get("categories") else "",
            "ingredients_text": product.get("ingredients_text", ""),
        })

    return results