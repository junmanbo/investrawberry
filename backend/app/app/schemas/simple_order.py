from pydantic import BaseModel
from typing import Optional

# Shared properties
class SimpleOrderBase(BaseModel):
    user_id: Optional[int] = None
    order_type_id: Optional[int] = None
    ticker_id: Optional[int] = None
    status: Optional[str] = None
    side: Optional[str] = None
    total_amount: Optional[float] = None
    duration: Optional[int] = None
    interval: Optional[int] = None
    count: Optional[int] = None
    single_amount: Optional[float] = None

# Properties to receive via API on creation
class SimpleOrderCreate(SimpleOrderBase):
    user_id: int
    order_type_id: int
    ticker_id: int
    status: str
    side: str
    total_amount: float
    duration: int
    interval: int
    count: int
    single_amount: float

# Properties to receive via API on update
class SimpleOrderUpdate(SimpleOrderBase):
    pass

class SimpleOrderInDBBase(SimpleOrderBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class SimpleOrder(SimpleOrderInDBBase):
    pass

# Additional properties stored in DB
class SimpleOrderInDB(SimpleOrderInDBBase):
    pass


class SimpleOrderTransactionBase(BaseModel):
    simple_order_id: Optional[int] = None
    uuid: Optional[str] = None
    price: Optional[float] = None
    amount: Optional[float] = None
    fee: Optional[float] = None

# Properties to receive via API on creation
class SimpleOrderTransactionCreate(SimpleOrderTransactionBase):
    simple_order_id: int
    uuid: str
    price: float
    amount: float

# Properties to receive via API on update
class SimpleOrderTransactionUpdate(SimpleOrderTransactionBase):
    pass

class SimpleOrderTransactionInDBBase(SimpleOrderTransactionBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class SimpleOrderTransaction(SimpleOrderTransactionInDBBase):
    pass

# Additional properties stored in DB
class SimpleOrderTransactionInDB(SimpleOrderTransactionInDBBase):
    pass

