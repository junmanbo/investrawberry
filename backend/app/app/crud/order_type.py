from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.order_type import OrderType
from app.schemas.order_type import OrderTypeCreate, OrderTypeUpdate


class CRUDOrderType(CRUDBase[OrderType, OrderTypeCreate, OrderTypeUpdate]):
    def get_by_name(self, db: Session, *, order_type_nm: str) -> Optional[OrderType]:
        return db.query(OrderType).filter(OrderType.order_type_nm == order_type_nm).first()


order_type = CRUDOrderType(OrderType)

