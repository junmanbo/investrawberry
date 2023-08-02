from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    ForeignKey,
    Text,
    Float,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Portfolio(Base):
    """포트폴리오"""

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    rebal_period = Column(Integer, nullable=False, default=365)
    memo = Column(Text)
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


class PortfolioOrder(Base):
    """포트폴리오 주문 내역"""

    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolio.id"))
    is_running = Column(Boolean(), nullable=False, default=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    portfolio = relationship("Portfolio", backref="portfolio_order")


class PortfolioTransaction(Base):
    """포트폴리오 주문의 매매 내역"""

    id = Column(Integer, primary_key=True, index=True)
    portfolio_order_id = Column(Integer, ForeignKey("portfolio_order.id"))
    uuid = Column(String, nullable=False)
    ticker_id = Column(Integer, ForeignKey("ticker.id"))
    order_type = Column(String(10))
    side = Column(String(10), nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    fee = Column(Float)
    is_fiiled = Column(Boolean(), nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    portfolio_order = relationship("PortfolioOrder", backref="portfolio_transaction")
    ticker = relationship("Ticker", backref="portfolio_transaction")
