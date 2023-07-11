from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Float
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class SimpleOrder(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    order_type_id = Column(Integer, ForeignKey("ordertype.id"))
    ticker_id = Column(Integer, ForeignKey("ticker.id"))
    status = Column(String(20), nullable=False)
    side = Column(String(10), nullable=False)
    total_amount = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    interval = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False)
    single_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="simple_order")

class SimpleOrderTransaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    simple_order_id = Column(Integer, ForeignKey("simpleorder.id"))
    uuid = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    fee = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    simple_order = relationship("SimpleOrder", backref="simple_order_transaction")
