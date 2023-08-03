from pydantic import BaseModel


# Portfolio
class PortfolioBase(BaseModel):
    user_id: int | None = None
    rebal_period: int | None = None
    is_running: bool | None = False
    amount: int | None = 0
    memo: str | None = None


class PortfolioCreate(PortfolioBase):
    user_id: int


class PortfolioUpdate(PortfolioBase):
    user_id: int
    rebal_period: int
    is_running: bool


class PortfolioInDBBase(PortfolioBase):
    id: int | None = None

    class Config:
        from_attributes = True


class Portfolio(PortfolioInDBBase):
    pass


class PortfolioInDB(PortfolioInDBBase):
    pass


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
    pass


class PortfolioTickerInDB(PortfolioTickerInDBBase):
    pass


# PortfolioTransaction
class PortfolioTransactionBase(BaseModel):
    portfolio_ticker_id: int | None = None
    uuid: str | None = None
    order_type: str | None = None
    side: str | None = None
    price: float | None = None
    quantity: float | None = None
    fee: float | None = None
    is_fiiled: bool | None = False


class PortfolioTransactionCreate(PortfolioTransactionBase):
    portfolio_ticker_id: int
    uuid: str
    side: str
    price: float
    quantity: float


class PortfolioTransactionUpdate(PortfolioTransactionBase):
    pass


class PortfolioTransactionInDBBase(PortfolioTransactionBase):
    id: int | None = None

    class Config:
        from_attributes = True


class PortfolioTransaction(PortfolioTransactionInDBBase):
    pass


class PortfolioTransactionInDB(PortfolioTransactionInDBBase):
    pass
