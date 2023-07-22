from pydantic import BaseModel
from typing import Optional

from app.schemas.ticker import Ticker

# Shared properties
class SimpleTransactionBase(BaseModel):
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
class SimpleTransactionCreate(SimpleTransactionBase):
    ticker_id: int
    order_type: str
    side: str
    price: float
    quantity: float

# Properties to receive via API on update
class SimpleTransactionUpdate(SimpleTransactionBase):
    uuid: str
    status: str

class SimpleTransactionInDBBase(SimpleTransactionBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class SimpleTransaction(SimpleTransactionInDBBase):
    ticker: Ticker

# Additional properties stored in DB
class SimpleTransactionInDB(SimpleTransactionInDBBase):
    pass

