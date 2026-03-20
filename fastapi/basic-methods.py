###  Implemented all the methods : GET, POST, PUT, DELETE
###  To run : uvicorn basic-methods:app --reload
###


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: int
    instock: str

items = {
    1: {
        "name": "Shirt",
        "price": 999,
        "instock": "y"
    }
}

@app.get("/items")
def get_items():
    """
    returns data available in items dictionary
    Returns -> dict
    """
    return items


@app.get("/items/{item_id}")
def get_items(item_id: int):
    """
    Takes item_id from the request URL and returns data available against it
    Returns -> dict
    """
    return items[item_id]


@app.post("/items")
def add_items(item: Item):
    """
    Allows adding items to the db (dictionary)
    takes values from the request payload and validates it against Item base class
    returns -> item_id of the added item
    """
    item_id = len(items)+1
    items[item_id] = item
    return {f"Item {item_id} added"}

@app.put("/items/{item_id}")
def update_items(item_id: int, item: Item):
    """
    Allows updating items to the db (dictionary)
    takes values from the request payload and validates it against Item base class
    returns -> item_id of the added item
    """
    if item_id in items:
        items[item_id] = item
        return {f"Item {item_id} updated"}
    else:
        return {f"Item {item_id} does not exists"}

@app.delete("/items/{item_id}")
def delete_items(item_id: int):
    """
    Allows deleting items from the db (dictionary)
    takes item_id from the request payload
    returns -> item_id of the deleted item
    """
    if item_id in items:
        items.pop(item_id)
        return {f"Item {item_id} deleted"}
    else:
        return {f"Item {item_id} does not exists"}

