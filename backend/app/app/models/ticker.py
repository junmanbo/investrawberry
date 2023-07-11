from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Ticker(Base):
    id = Column(Integer, primary_key=True, index=True)
    exchange_id = Column(Integer, ForeignKey("exchange.id"))
    symbol = Column(String(50), nullable=False)
    currency = Column(String(50), nullable=False)
    ticker_knm = Column(String(50))
    ticker_type = Column(String(10), nullable=False)
    is_coin = Column(Boolean(), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    exchange = relationship("Exchange", backref="exchange_keys")

