import requests

BASE_URL = "https://world.openfoodfacts.org/api/v2/product"
HEADERS = {"User-Agent": "InventoryManagementApp/1.0 (student project)"}


def fetch_product_by_barcode(barcode):
    """
    Fetch product details from OpenFoodFacts by barcode.
    Returns a dict with the fields we care about, or None if not found/error.
    """
    url = f"{BASE_URL}/{barcode}.json"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return None

    data = response.json()

    if data.get("status") != 1:
        return None

    product = data["product"]
    return {
        "barcode": barcode,
        "name": product.get("product_name"),
        "brand": product.get("brands"),
        "ingredients_text": product.get("ingredients_text"),
    }