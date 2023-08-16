from pydantic import BaseModel
from typing import List
from datetime import date

from .ticker import Ticker


# PortfolioTicker
class PortfolioTickerBase(BaseModel):
    portfolio_id: int | None = None
    ticker_id: int | None = None
    weight: int | None = None


class PortfolioTickerCreate(PortfolioTickerBase):
    portfolio_id: int
    ticker_id: int
    weight: int


class PortfolioTickerUpdate(PortfolioTickerBase):
    pass


class PortfolioTickerInDBBase(PortfolioTickerBase):
    id: int | None = None

    class Config:
        from_attributes = True


class PortfolioTicker(PortfolioTickerInDBBase):
    ticker: Ticker


class PortfolioTickerInDB(PortfolioTickerInDBBase):
    pass


# Portfolio
class PortfolioBase(BaseModel):
    user_id: int | None = None
    rebal_period: int | None = None
    is_running: bool | None = False
    amount: int | None = 0
    memo: str | None = None
    rebal_dt: date | None = None


class PortfolioCreate(PortfolioBase):
    user_id: int


class PortfolioUpdate(PortfolioBase):
    pass


class PortfolioInDBBase(PortfolioBase):
    id: int | None = None

    class Config:
        from_attributes = True


class Portfolio(PortfolioInDBBase):
    portfolio_ticker: List[PortfolioTicker] = []


class PortfolioInDB(PortfolioInDBBase):
    pass
