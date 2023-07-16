from pydantic import BaseModel
from typing import Optional

# Shared properties
class SimpleTransactionBase(BaseModel):
    user_id: Optional[int] = None
    uuid: Optional[str] = None
    ticker_id: Optional[int] = None
    order_type_id: Optional[int] = None
    side: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[float] = None
    fee: Optional[float] = None
    is_filled: Optional[bool] = None

# Properties to receive via API on creation
class SimpleTransactionCreate(SimpleTransactionBase):
    user_id: int
    uuid: str
    ticker_id: int
    order_type_id: int
    side: str
    price: float
    quantity: float
    is_filled: bool

# Properties to receive via API on update
class SimpleTransactionUpdate(SimpleTransactionBase):
    pass

class SimpleTransactionInDBBase(SimpleTransactionBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class SimpleTransaction(SimpleTransactionInDBBase):
    pass

# Additional properties stored in DB
class SimpleTransactionInDB(SimpleTransactionInDBBase):
    pass

