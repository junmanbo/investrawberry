from pydantic import BaseModel
from typing import Optional


# Shared properties
class StrategyBase(BaseModel):
    strategy_nm: Optional[str] = None
    strategy_knm: Optional[str] = None
    strategy_desc: Optional[str] = None


# Properties to receive via API on creation
class StrategyCreate(StrategyBase):
    strategy_nm: str
    strategy_knm: str


# Properties to receive via API on update
class StrategyUpdate(StrategyBase):
    pass


class StrategyInDBBase(StrategyBase):
    id: Optional[int] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class Strategy(StrategyInDBBase):
    pass


# Additional properties stored in DB
class StrategyInDB(StrategyInDBBase):
    pass
