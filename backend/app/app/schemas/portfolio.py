from pydantic import BaseModel
from typing import Optional

# Portfolio
class PortfolioBase(BaseModel):
    user_id: Optional[int] = None
    ticker_id: Optional[int] = None
    weight: Optional[int] = None
    rebal_period: Optional[int] = None

class PortfolioCreate(PortfolioBase):
    user_id: int
    ticker_id: int

class PortfolioUpdate(PortfolioBase):
    pass

class PortfolioInDBBase(PortfolioBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

class Portfolio(PortfolioInDBBase):
    pass

class PortfolioInDB(PortfolioInDBBase):
    pass


# PortfolioMemo
class PortfolioMemoBase(BaseModel):
    portfolio_id: Optional[int] = None
    content: Optional[str] = None

class PortfolioMemoCreate(PortfolioMemoBase):
    portfolio_id: int
    content: str

class PortfolioMemoUpdate(PortfolioMemoBase):
    pass

class PortfolioMemoInDBBase(PortfolioMemoBase):
    portfolio_id: int

    class Config:
        orm_mode = True

class PortfolioMemo(PortfolioMemoInDBBase):
    pass

class PortfolioMemoInDB(PortfolioMemoInDBBase):
    pass


# PortfolioOrder
class PortfolioOrderBase(BaseModel):
    portfolio_id: Optional[int] = None
    strategy_id: Optional[int] = None
    is_running: Optional[bool] = None
    amount: Optional[int] = None

class PortfolioOrderCreate(PortfolioOrderBase):
    portfolio_id: int
    strategy_id: int
    amount: int

class PortfolioOrderUpdate(PortfolioOrderBase):
    pass

class PortfolioOrderInDBBase(PortfolioOrderBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

class PortfolioOrder(PortfolioOrderInDBBase):
    pass

class PortfolioOrderInDB(PortfolioOrderInDBBase):
    pass


# PortfolioTransaction
class PortfolioTransactionBase(BaseModel):
    portfolio_order_id: Optional[int] = None
    uuid: Optional[str] = None
    ticker_id: Optional[int] = None
    order_type: Optional[str] = None
    side: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[float] = None
    fee: Optional[float] = None
    is_filled: Optional[bool] = None

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
    id: Optional[int] = None

    class Config:
        orm_mode = True

class PortfolioTransaction(PortfolioTransactionInDBBase):
    pass

class PortfolioTransactionInDB(PortfolioTransactionInDBBase):
    pass

