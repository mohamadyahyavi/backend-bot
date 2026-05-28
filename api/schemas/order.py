from pydantic import BaseModel
from typing import Optional


# -----------------------------
# CREATE ORDER
# -----------------------------
class OrderCreate(BaseModel):
    user_id: int
    total_price: float


# -----------------------------
# ORDER RESPONSE
# -----------------------------
class OrderResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    status: str

    class Config:
        from_attributes = True


# -----------------------------
# ADD ORDER ITEM
# -----------------------------
class OrderItemCreate(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price: float


# -----------------------------
# ORDER ITEM RESPONSE
# -----------------------------
class OrderItemResponse(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True