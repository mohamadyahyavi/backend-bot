from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.database import SessionLocal
from api.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


# -----------------------------
# DB dependency
# -----------------------------
async def get_db():
    async with SessionLocal() as session:
        yield session


# -----------------------------
# TELEGRAM LOGIN / REGISTER
# -----------------------------
@router.post("/telegram")
async def telegram_auth(
    telegram_id: int,
    username: str | None = None,
    first_name: str | None = None,
    db: AsyncSession = Depends(get_db)
):

    # 1. check if user exists
    result = await db.execute(
        select(User).where(User.telegram_id == telegram_id)
    )

    user = result.scalar_one_or_none()

    # -------------------------
    # LOGIN CASE
    # -------------------------
    if user:
        return {
            "status": "login",
            "message": "User already exists",
            "user_id": user.id
        }

    # -------------------------
    # REGISTER CASE
    # -------------------------
    new_user = User(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {
        "status": "registered",
        "message": "New user created",
        "user_id": new_user.id
    }