from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.exchange_key import ExchangeKey
from app.schemas.exchange_key import ExchangeKeyCreate, ExchangeKeyUpdate


class CRUDExchangeKey(CRUDBase[ExchangeKey, ExchangeKeyCreate, ExchangeKeyUpdate]):
    def get_multi_by_owner(self, db: Session, *, owner_id: int) -> List[ExchangeKey]:
        return db.query(ExchangeKey).filter(ExchangeKey.user_id == owner_id).all()

    def get_key_by_owner_exchange(self, db: Session, *, owner_id: int, exchange_id: int) -> ExchangeKey:
        return db.query(ExchangeKey).filter(ExchangeKey.user_id == owner_id,
                                            ExchangeKey.exchange_id == exchange_id).first()


exchange_key = CRUDExchangeKey(ExchangeKey)

