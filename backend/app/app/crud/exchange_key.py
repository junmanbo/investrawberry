from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.exchange_key import ExchangeKey
from app.schemas.exchange_key import ExchangeKeyCreate, ExchangeKeyUpdate


class CRUDExchangeKey(CRUDBase[ExchangeKey, ExchangeKeyCreate, ExchangeKeyUpdate]):
    def get_multi_by_owner(self, db: Session, *, owner_id: int, skip: int, limit: int) -> List[ExchangeKey]:
        return db.query(ExchangeKey).offset(skip).limit(limit).filter(ExchangeKey.user_id == owner_id).all()



exchange_key = CRUDExchangeKey(ExchangeKey)

