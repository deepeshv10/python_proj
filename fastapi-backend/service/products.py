import json
from pathlib import Path
from typing import Optional, Dict

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "products.json"

def load_products() -> list[Dict]:
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def get_products_by_name(name: str) -> Optional[Dict]:
    products = load_products()
    matching_products = []
    for product in products:
        if name.lower() in product["name"].lower():
            matching_products.append(product)
    if matching_products:
        return matching_products
    return None


def get_products_by_category(category: str) -> Optional[Dict]:
    products = load_products()
    matching_products = []
    for product in products:
        if category.lower() in product["category"].lower():
            matching_products.append(product)
    if matching_products:
        return matching_products
    return None