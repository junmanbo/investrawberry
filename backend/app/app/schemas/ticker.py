from pydantic import BaseModel

from app import schemas


# Shared properties
class TickerBase(BaseModel):
    exchange_id: int | None = None
    asset_type_id: int | None = None
    symbol: str | None = None
    currency: str | None = None
    ticker_knm: str | None = None
    marketcap: int | None = None
    price: int | None = None
    maker_fee: float | None = None
    taker_fee: float | None = None


# Properties to receive via API on creation
class TickerCreate(TickerBase):
    exchange_id: int
    asset_type_id: int
    symbol: str
    currency: str


# Properties to receive via API on update
class TickerUpdate(TickerBase):
    marketcap: int
    price: int


class TickerInDBBase(TickerBase):
    id: int | None = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class Ticker(TickerInDBBase):
    pass


# Additional properties stored in DB
class TickerInDB(TickerInDBBase):
    pass
