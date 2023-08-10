from pydantic import BaseModel
from typing import Optional

from app.schemas.ticker import Ticker


# Shared properties
class TransactionBase(BaseModel):
    user_id: Optional[int] = None
    ticker_id: Optional[int] = None
    uuid: Optional[str] = None
    order_type: Optional[str] = None
    side: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[float] = None
    fee: Optional[float] = None
    status: Optional[str] = None


# Properties to receive via API on creation
class TransactionCreate(TransactionBase):
    ticker_id: int
    order_type: str
    side: str
    price: float
    quantity: float


# Properties to receive via API on update
class TransactionUpdate(TransactionBase):
    uuid: str
    status: str


class TransactionInDBBase(TransactionBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class Transaction(TransactionInDBBase):
    ticker: Ticker


# Additional properties stored in DB
class TransactionInDB(TransactionInDBBase):
    pass
