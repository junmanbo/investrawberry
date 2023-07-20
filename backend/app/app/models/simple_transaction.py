from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Float, Boolean
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class SimpleTransaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    ticker_id = Column(Integer, ForeignKey("ticker.id"))
    uuid = Column(String)
    order_type = Column(String(10))
    side = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    fee = Column(Float)
    is_filled = Column(Boolean(), default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="simple_transaction")
    ticker = relationship("Ticker", backref="simple_transaction")
