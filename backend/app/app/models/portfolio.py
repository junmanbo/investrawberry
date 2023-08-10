from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    ForeignKey,
    Text,
    Date,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Portfolio(Base):
    """포트폴리오"""

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    rebal_period = Column(Integer, nullable=False, default=365)
    is_running = Column(Boolean(), nullable=False, default=False)
    amount = Column(Integer, nullable=False, default=0)
    memo = Column(Text)
    rebal_dt = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", backref="portfolio")


class PortfolioTicker(Base):
    """포트폴리오 티커 구성"""

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolio.id"))
    ticker_id = Column(Integer, ForeignKey("ticker.id"))
    weight = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    portfolio = relationship("Portfolio", backref="portfolio_ticker")
    ticker = relationship("Ticker", backref="portfolio_ticker")
