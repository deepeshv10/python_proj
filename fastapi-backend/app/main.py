from fastapi import FastAPI, HTTPException, Query
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

app = FastAPI()


@app.get("/health")
def root():
    return {"status": "ok"}


@app.get("/products/", response_model=list[Product])
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
    return products


@app.get("/products/{product_id}", response_model=Product)
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