from pydantic import BaseModel

from app import schemas


# Shared properties
class ExchangeKeyBase(BaseModel):
    exchange_id: int | None = None
    user_id: int | None = None
    access_key: str | None = None
    secret_key: str | None = None
    account: str | None = None
    is_valid: bool | None = True


# Properties to receive via API on creation
class ExchangeKeyCreate(ExchangeKeyBase):
    access_key: str
    secret_key: str
    account: str | None = None


# Properties to receive via API on update
class ExchangeKeyUpdate(ExchangeKeyBase):
    pass


class ExchangeKeyInDBBase(ExchangeKeyBase):
    id: int | None = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class ExchangeKey(BaseModel):
    id: int
    is_valid: bool
    exchange: schemas.Exchange


# Additional properties stored in DB
class ExchangeKeyInDB(ExchangeKeyInDBBase):
    pass
