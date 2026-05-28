from pydantic import BaseModel
from typing import Optional


# -----------------------------
# CREATE PRODUCT
# -----------------------------
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int = 0


# -----------------------------
# UPDATE PRODUCT
# -----------------------------
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None


# -----------------------------
# PRODUCT RESPONSE
# -----------------------------
class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock: int

    class Config:
        from_attributes = True