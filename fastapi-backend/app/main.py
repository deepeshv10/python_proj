from fastapi import FastAPI, HTTPException, Query
from service.products import get_products_by_id
app = FastAPI()

@app.get("/health")
def root():
    return {"status": "ok"}

@app.get("/products/")
def get_products(
    name: str = Query(
        default="",
        min_length=3,
        examples="Smartphone",
        description="The name of the product"),
    category: str = Query(
        default="",
        min_length=3,
        examples="Smartphone",
        description="The name of the product")
    ):
    """
    Get a product by name
    Args:
        name: The name of the product
    Returns:
        The product(s)
    Raises:
        HTTPException: If the product is not found
    """
    products = get_products_by_id(name)
    if products:
        return products
    else:
        raise HTTPException(status_code=404, detail=f"Product with {name} not found")
