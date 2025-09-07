from typing import Optional, List
from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int

class ProductRead(BaseModel):
    id: int
    name: str
    price: float
    stock: int

class CartItem(BaseModel):
    product_id: int
    quantity: int

class CheckoutRequest(BaseModel):
    items: List[CartItem]

class Order(BaseModel):
    user: str
    items: List[CartItem]
    total: float

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    