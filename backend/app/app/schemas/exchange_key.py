from pydantic import BaseModel
from typing import Optional

# Shared properties
class ExchangeKeyBase(BaseModel):
    exchange_id: Optional[int] = None
    user_id: Optional[int] = None
    access_key: Optional[str] = None
    secret_key: Optional[str] = None
    account: Optional[str] = None
    is_valid: Optional[bool] = True

# Properties to receive via API on creation
class ExchangeKeyCreate(ExchangeKeyBase):
    exchange_id: int
    user_id: int
    access_key: str
    secret_key: str

# Properties to receive via API on update
class ExchangeKeyUpdate(ExchangeKeyBase):
    pass

class ExchangeKeyInDBBase(ExchangeKeyBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class ExchangeKey(ExchangeKeyInDBBase):
    pass

# Additional properties stored in DB
class ExchangeKeyInDB(ExchangeKeyInDBBase):
    pass

