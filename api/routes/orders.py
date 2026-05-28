from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.database import SessionLocal
from api.models.user import User
from api.models.order import Order

router = APIRouter(prefix="/orders", tags=["Orders"])


# -----------------------------
# DB Dependency
# -----------------------------
async def get_db():
    async with SessionLocal() as session:
        yield session


# -----------------------------
# GET OR CREATE USER (IMPORTANT)
# -----------------------------
async def get_or_create_user(telegram_id: int, db: AsyncSession):

    result = await db.execute(
        select(User).where(User.telegram_id == telegram_id)
    )

    user = result.scalar_one_or_none()

    if user:
        return user

    # اگر کاربر وجود نداشت → ساخته می‌شود
    user = User(
        telegram_id=telegram_id,
        username=None,
        first_name="Unknown"
    )

    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


# -----------------------------
# CREATE ORDER
# -----------------------------
@router.post("/")
async def create_order(
    telegram_id: int,
    total_price: float,
    db: AsyncSession = Depends(get_db)
):

    # 1. گرفتن یا ساخت کاربر
    user = await get_or_create_user(telegram_id, db)

    # 2. ساخت سفارش با user_id (نه telegram_id)
    order = Order(
        user_id=user.id,
        total_price=total_price,
        status="pending"
    )

    db.add(order)
    await db.commit()
    await db.refresh(order)

    # 3. پاسخ
    return {
        "order_id": order.id,
        "user_id": user.id,
        "telegram_id": user.telegram_id,
        "username": user.username,
        "first_name": user.first_name
    }