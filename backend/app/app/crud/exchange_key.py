from app.crud.base import CRUDBase
from app.models.exchange_key import ExchangeKey
from app.schemas.exchange_key import ExchangeKeyCreate, ExchangeKeyUpdate


class CRUDExchangeKey(CRUDBase[ExchangeKey, ExchangeKeyCreate, ExchangeKeyUpdate]):
    pass


exchange_key = CRUDExchangeKey(ExchangeKey)

