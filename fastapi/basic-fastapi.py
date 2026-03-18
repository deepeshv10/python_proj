# run as : uvicorn basic-fastapi:app --reload

from fastapi import FastAPI
from pydantic import BaseModel

# 1. Initialize the FastAPI app
app = FastAPI()

# 2. Define a Pydantic model for POST data validation
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

# 3. A basic GET endpoint
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI !"}

# 4. A POST endpoint that receives a JSON body
@app.post("/items/")
def create_item(item: Item):
    # Here you would typically save 'item' to a database
    return {"status": "item created", "data": item}