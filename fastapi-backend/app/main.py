from fastapi import FastAPI, HTTPException, Query, Depends
from service.products import (
    Product,
    ProductCreate,
    ProductUpdate,
    get_products_by_name,
    get_products_by_category,
    get_product_by_id,
    create_product,
    update_product,
    delete_product,
)
from service.orders import (
    Order,
    OrderCreate,
    get_all_orders,
    get_order_by_id,
    create_order,
)

app = FastAPI()

def say_hello():
    return "Welcome to my Fastapi app"

@app.get("/health")
def root(depends=Depends(say_hello)):       # example of dependency injection
    return {"status": f"{depends}. App is ok"}


@app.get("/products/")
def search_products(
    name: str = Query(
        default="",
        min_length=3,
        examples=["Smartphone"],
        description="The name of the product",
    ),
):
    products = get_products_by_name(name)
    if not products:
        raise HTTPException(status_code=404, detail=f"No products matching '{name}'")
    return { "total products": len(products), "products": products}


@app.get("/products/{product_id}")
def get_product(product_id: int):
    product = get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product


@app.post("/products/", response_model=Product, status_code=201)
def create_new_product(data: ProductCreate):
    return create_product(data)


@app.patch("/products/{product_id}", response_model=Product)
def patch_product(product_id: int, data: ProductUpdate):
    product = update_product(product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product


@app.delete("/products/{product_id}", response_model=Product)
def remove_product(product_id: int):
    product = delete_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product {product_id} not found")
    return product


# ── Orders ───────────────────────────────────────────────────────────


@app.get("/orders/", response_model=list[Order])
def list_orders():
    return get_all_orders()


@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    order = get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return order


@app.post("/orders/", response_model=Order, status_code=201)
def place_order(data: OrderCreate):
    try:
        return create_order(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

