from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.database import SessionLocal
from api.models.product import Product

router = APIRouter(prefix="/products", tags=["Products"])


# -----------------------------
# DB dependency
# -----------------------------
async def get_db():
    async with SessionLocal() as session:
        yield session


# -----------------------------
# GET ALL PRODUCTS
# -----------------------------
@router.get("/")
async def get_products(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Product))
    products = result.scalars().all()

    return products


# -----------------------------
# GET SINGLE PRODUCT
# -----------------------------
@router.get("/{product_id}")
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )

    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


# -----------------------------
# CREATE PRODUCT
# -----------------------------
@router.post("/")
async def create_product(
    name: str,
    price: float,
    stock: int = 0,
    db: AsyncSession = Depends(get_db)
):

    product = Product(
        name=name,
        price=price,
        stock=stock
    )

    db.add(product)
    await db.commit()
    await db.refresh(product)

    return product


# -----------------------------
# UPDATE PRODUCT
# -----------------------------
@router.put("/{product_id}")
async def update_product(
    product_id: int,
    name: str | None = None,
    price: float | None = None,
    stock: int | None = None,
    db: AsyncSession = Depends(get_db)
):

    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )

    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if name is not None:
        product.name = name

    if price is not None:
        product.price = price

    if stock is not None:
        product.stock = stock

    await db.commit()
    await db.refresh(product)

    return product


# -----------------------------
# DELETE PRODUCT
# -----------------------------
@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(Product).where(Product.id == product_id)
    )

    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    await db.delete(product)
    await db.commit()

    return {"message": "Product deleted successfully"}