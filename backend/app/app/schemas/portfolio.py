from pydantic import BaseModel
from typing import Optional

# Shared properties
class PortfolioBase(BaseModel):
    user_id: Optional[int] = None
    ticker_id: Optional[int] = None
    weight: Optional[int] = 100
    rebal_period: Optional[int] = 365
    is_running: Optional[bool] = False

# Properties to receive via API on creation
class PortfolioCreate(PortfolioBase):
    user_id: int
    ticker_id: int

# Properties to receive via API on update
class PortfolioUpdate(PortfolioBase):
    pass

class PortfolioInDBBase(PortfolioBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class Portfolio(PortfolioInDBBase):
    pass

# Additional properties stored in DB
class PortfolioInDB(PortfolioInDBBase):
    pass


class PortfolioMemoBase(BaseModel):
    content: Optional[str] = None

# Properties to receive via API on creation
class PortfolioMemoCreate(PortfolioMemoBase):
    portfolio_id: int

# Properties to receive via API on update
class PortfolioMemoUpdate(PortfolioMemoBase):
    pass

class PortfolioMemoInDBBase(PortfolioMemoBase):
    portfolio_id: int

    class Config:
        orm_mode = True

# Additional properties to return via API
class PortfolioMemo(PortfolioMemoInDBBase):
    pass

# Additional properties stored in DB
class PortfolioMemoInDB(PortfolioMemoInDBBase):
    pass

