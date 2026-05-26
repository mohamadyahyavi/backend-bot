from sqlalchemy import Column, Integer, String
from api.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    telegram_id = Column(Integer, unique=True, nullable=False)

    username = Column(String, nullable=True)

    first_name = Column(String, nullable=False)