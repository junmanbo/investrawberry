from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.exchange import Exchange
from app.schemas.exchange import ExchangeCreate, ExchangeUpdate


class CRUDExchange(CRUDBase[Exchange, ExchangeCreate, ExchangeUpdate]):
    def get_by_name(self, db: Session, *, exchange_nm) -> Optional[Exchange]:
        return db.query(Exchange).filter(Exchange.exchange_nm == exchange_nm).first()


exchange = CRUDExchange(Exchange)

