from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.asset_type import AssetType
from app.schemas.asset_type import AssetTypeCreate, AssetTypeUpdate


class CRUDAssetType(CRUDBase[AssetType, AssetTypeCreate, AssetTypeUpdate]):
    def get_by_name(self, db: Session, *, asset_nm: str) -> Optional[AssetType]:
        return db.query(AssetType).filter(AssetType.asset_nm == asset_nm).first()


asset_type = CRUDAssetType(AssetType)

