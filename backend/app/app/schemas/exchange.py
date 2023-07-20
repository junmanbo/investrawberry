from pydantic import BaseModel
from datetime import time
from typing import Optional

# Shared properties
class ExchangeBase(BaseModel):
    exchange_nm: Optional[str] = None
    exchange_knm: Optional[str] = None
    open_time: Optional[time] = None
    close_time: Optional[time] = None
    is_summer: Optional[bool] = None
    min_interval: Optional[int] = None
    min_amount: Optional[int] = None
    min_digit: Optional[int] = None

# Properties to receive via API on creation
class ExchangeCreate(ExchangeBase):
    exchange_nm: str
    open_time: time
    close_time: time
    is_summer: bool
    min_interval: int

# Properties to receive via API on update
class ExchangeUpdate(ExchangeBase):
    pass

class ExchangeInDBBase(ExchangeBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class Exchange(ExchangeInDBBase):
    pass

# Additional properties stored in DB
class ExchangeInDB(ExchangeInDBBase):
    pass

