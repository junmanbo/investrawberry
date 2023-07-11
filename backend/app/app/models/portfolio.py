from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Portfolio(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    ticker_id = Column(Integer, ForeignKey("ticker.id"))
    weight = Column(Integer, nullable=False, default=100)
    rebal_period = Column(Integer, nullable=False, default=365)
    is_running = Column(Boolean(), nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ticker = relationship("Ticker", backref="portfolio")


class PortfolioMemo(Base):
    portfolio = Column(Integer, ForeignKey("portfolio.id"))
    content = Column(Text)

