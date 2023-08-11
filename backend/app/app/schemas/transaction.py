from pydantic import BaseModel
from typing import Optional

from app.schemas.ticker import Ticker


# Shared properties
class TransactionBase(BaseModel):
    user_id: int | None = None
    ticker_id: int | None = None
    uuid: str | None = None
    order_type: str | None = None
    side: str | None = None
    price: float | None = None
    quantity: float | None = None
    fee: float | None = None
    status: str | None = None


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
    id: int | None = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class Transaction(TransactionInDBBase):
    ticker: Ticker


# Additional properties stored in DB
class TransactionInDB(TransactionInDBBase):
    pass
