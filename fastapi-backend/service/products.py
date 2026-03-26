import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from pydantic import BaseModel

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "products.json"


class Product(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    brand: str
    sku: str
    stock: int
    rating: float
    tags: list[str]
    is_active: bool
    created_at: str
    updated_at: str


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    category: str
    brand: str
    sku: str
    stock: int = 0
    rating: float = 0.0
    tags: list[str] = []
    is_active: bool = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    sku: Optional[str] = None
    stock: Optional[int] = None
    rating: Optional[float] = None
    tags: Optional[list[str]] = None
    is_active: Optional[bool] = None


_products_cache: list[Product] | None = None


def _load_products() -> list[Product]:
    global _products_cache
    if _products_cache is None:
        with open(DATA_FILE) as f:
            _products_cache = [Product(**item) for item in json.load(f)]
    return _products_cache


def _save_products() -> None:
    with open(DATA_FILE, "w") as f:
        json.dump([p.model_dump() for p in _load_products()], f, indent=2)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _next_id() -> int:
    products = _load_products()
    return max(p.id for p in products) + 1 if products else 1


def _search(field: str, query: str) -> list[Product]:
    q = query.lower()
    return [p for p in _load_products() if q in getattr(p, field).lower()]


def get_products_by_name(name: str) -> list[Product]:
    return _search("name", name)


def get_products_by_category(category: str) -> list[Product]:
    return _search("category", category)


def get_product_by_id(product_id: int) -> Optional[Product]:
    return next((p for p in _load_products() if p.id == product_id), None)


def create_product(data: ProductCreate) -> Product:
    now = _now_iso()
    product = Product(
        id=_next_id(),
        **data.model_dump(),
        created_at=now,
        updated_at=now,
    )
    _load_products().append(product)
    _save_products()
    return product


def update_product(product_id: int, data: ProductUpdate) -> Optional[Product]:
    products = _load_products()
    for i, p in enumerate(products):
        if p.id == product_id:
            updated = p.model_copy(
                update={**data.model_dump(exclude_unset=True), "updated_at": _now_iso()}
            )
            products[i] = updated
            _save_products()
            return updated
    return None


def delete_product(product_id: int) -> Optional[Product]:
    products = _load_products()
    for i, p in enumerate(products):
        if p.id == product_id:
            removed = products.pop(i)
            _save_products()
            return removed
    return None