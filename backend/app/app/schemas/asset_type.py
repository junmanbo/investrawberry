from pydantic import BaseModel
from typing import Optional

# Shared properties
class AssetTypeBase(BaseModel):
    asset_nm: Optional[str] = None
    asset_knm: Optional[str] = None

# Properties to receive via API on creation
class AssetTypeCreate(AssetTypeBase):
    asset_nm: str
    asset_knm: str

# Properties to receive via API on update
class AssetTypeUpdate(AssetTypeBase):
    pass

class AssetTypeInDBBase(AssetTypeBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True

# Additional properties to return via API
class AssetType(AssetTypeInDBBase):
    pass

# Additional properties stored in DB
class AssetTypeInDB(AssetTypeInDBBase):
    pass

