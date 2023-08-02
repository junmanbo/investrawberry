from pydantic import BaseModel


# Portfolio
class PortfolioBase(BaseModel):
    user_id: int | None = None
    rebal_period: int | None = None
    memo: str | None = None


class PortfolioCreate(PortfolioBase):
    user_id: int
    rebal_period: int


class PortfolioUpdate(PortfolioBase):
    user_id: int
    rebal_period: int


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
    ticker_id: int
    weight: int


class PortfolioTickerInDBBase(PortfolioTickerBase):
    portfolio_id: int

    class Config:
        from_attributes = True


class PortfolioTicker(PortfolioTickerInDBBase):
    pass


class PortfolioTickerInDB(PortfolioTickerInDBBase):
    pass


# PortfolioOrder
class PortfolioOrderBase(BaseModel):
    portfolio_id: int | None = None
    is_running: bool | None = None
    amount: int | None = None


class PortfolioOrderCreate(PortfolioOrderBase):
    portfolio_id: int
    amount: int


class PortfolioOrderUpdate(PortfolioOrderBase):
    pass


class PortfolioOrderInDBBase(PortfolioOrderBase):
    id: int | None = None

    class Config:
        from_attributes = True


class PortfolioOrder(PortfolioOrderInDBBase):
    pass


class PortfolioOrderInDB(PortfolioOrderInDBBase):
    pass


# PortfolioTransaction
class PortfolioTransactionBase(BaseModel):
    portfolio_order_id: int | None = None
    uuid: str | None = None
    ticker_id: int | None = None
    order_type: str | None = None
    side: str | None = None
    price: float | None = None
    quantity: float | None = None
    fee: float | None = None
    is_filled: bool | None = None


class PortfolioTransactionCreate(PortfolioTransactionBase):
    portfolio_order_id: int
    uuid: str
    ticker_id: int
    order_type: str
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
