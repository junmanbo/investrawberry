from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, Float, Enum
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Transaction(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    ticker_id = Column(Integer, ForeignKey("ticker.id"))
    uuid = Column(String)
    order_type = Column(Enum("market", "limit"))
    side = Column(Enum("buy", "sell"), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    fee = Column(Float)
    status = Column(Enum("open", "canceled", "closed"), default="open")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="transaction")
    ticker = relationship("Ticker", backref="transaction")
