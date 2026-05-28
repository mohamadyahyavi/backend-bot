from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from api.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    total_price = Column(Float, nullable=False)

    status = Column(String, default="pending")
    items = relationship("order_items", backref="order")