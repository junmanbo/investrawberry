from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Enum
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Ticker(Base):
    id = Column(Integer, primary_key=True, index=True)
    exchange_id = Column(Integer, ForeignKey("exchange.id"))
    asset_type = Column(Enum("kr_stock", "us_stock", "crypto", name="asset_type"))
    symbol = Column(String(50), nullable=False, unique=True)
    currency = Column(String(50), nullable=False)
    ticker_knm = Column(String(50))
    marketcap = Column(Integer)
    price = Column(Integer)
    maker_fee = Column(Float)
    taker_fee = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    exchange = relationship("Exchange", backref="ticker")
