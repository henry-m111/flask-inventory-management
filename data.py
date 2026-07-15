from external_api import fetch_product_by_barcode
import models

# Real barcodes to merge the inventory with actual OpenFoodFacts data
barcodes = [
    "3017620422003",   # Nutella
    "5059319023533",   # Rice Krispies
    "5000442007594",   # Olive oil
    "3760049790214",   # Pain De Mie Bio (bread)
]

def seed_inventory():
    """Fetch real product data and add it to the shared models.inventory store."""
    for barcode in barcodes:
        product = fetch_product_by_barcode(barcode)
        if product:
            models.add_item({
                "name": product["name"],
                "quantity": 10,
                "price": 100.0,
            })