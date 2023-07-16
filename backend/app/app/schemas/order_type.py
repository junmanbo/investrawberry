from pydantic import BaseModel
from typing import Optional

# Shared properties
class OrderTypeBase(BaseModel):
    order_type_nm: Optional[str] = None
    order_type_knm: Optional[str] = None

# Properties to receive via API on creation
class OrderTypeCreate(OrderTypeBase):
    order_type_nm: str
    order_type_knm: str

# Properties to receive via API on update
class OrderTypeUpdate(OrderTypeBase):
    pass

class OrderTypeInDBBase(OrderTypeBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class OrderType(OrderTypeInDBBase):
    pass

# Additional properties stored in DB
class OrderTypeInDB(OrderTypeInDBBase):
    pass

