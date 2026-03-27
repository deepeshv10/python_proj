import json
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

from service.products import get_product_by_id, update_product, ProductUpdate

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "orders.json"


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Order(BaseModel):
    id: int
    product_id: int
    quantity: int
    total_price: float
    status: OrderStatus
    created_at: str
    updated_at: str


class OrderCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, description="Must be at least 1")


_orders_cache: list[Order] | None = None


def _load_orders() -> list[Order]:
    global _orders_cache
    if _orders_cache is None:
        with open(DATA_FILE) as f:
            _orders_cache = [Order(**item) for item in json.load(f)]
    return _orders_cache


def _save_orders() -> None:
    with open(DATA_FILE, "w") as f:
        json.dump([o.model_dump() for o in _load_orders()], f, indent=2)


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _next_id() -> int:
    orders = _load_orders()
    return max(o.id for o in orders) + 1 if orders else 1


def get_all_orders() -> list[Order]:
    return _load_orders()


def get_order_by_id(order_id: int) -> Optional[Order]:
    return next((o for o in _load_orders() if o.id == order_id), None)


def create_order(data: OrderCreate) -> Order:
    product = get_product_by_id(data.product_id)
    if not product:
        raise ValueError(f"Product {data.product_id} not found")

    if product.stock < data.quantity:
        raise ValueError(
            f"Insufficient stock for '{product.name}': "
            f"requested {data.quantity}, available {product.stock}"
        )

    update_product(product.id, ProductUpdate(stock=product.stock - data.quantity))

    now = _now_iso()
    order = Order(
        id=_next_id(),
        product_id=data.product_id,
        quantity=data.quantity,
        total_price=round(product.price * data.quantity, 2),
        status=OrderStatus.PENDING,
        created_at=now,
        updated_at=now,
    )
    _load_orders().append(order)
    _save_orders()
    return order
