from pydantic import BaseModel
from typing import Optional


# -----------------------------
# TELEGRAM AUTH REQUEST
# -----------------------------
class TelegramAuthSchema(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: str


# -----------------------------
# USER RESPONSE
# -----------------------------
class UserResponse(BaseModel):
    id: int
    telegram_id: int
    username: Optional[str] = None
    first_name: str

    class Config:
        from_attributes = True