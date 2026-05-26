from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.database import SessionLocal
from api.models.order import Order
from api.models.order_item import OrderItem

router = APIRouter(prefix="/orders", tags=["Orders"])


async def get_db():
    async with SessionLocal() as session:
        yield session


@router.post("/")
async def create_order(
    user_id: int,
    total_price: float,
    db: AsyncSession = Depends(get_db)
):

    order = Order(
        user_id=user_id,
        total_price=total_price,
        status="pending"
    )

    db.add(order)
    await db.commit()
    await db.refresh(order)

    return order


@router.post("/item")
async def add_order_item(
    order_id: int,
    product_id: int,
    quantity: int,
    price: float,
    db: AsyncSession = Depends(get_db)
):

    item = OrderItem(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        price=price
    )

    db.add(item)
    await db.commit()
    await db.refresh(item)

    return item