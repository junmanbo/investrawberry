from typing import Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.ticker import Ticker
from app.schemas.ticker import TickerCreate, TickerUpdate


class CRUDTicker(CRUDBase[Ticker, TickerCreate, TickerUpdate]):
    def get_by_symbol(self, db: Session, *, symbol: str) -> Optional[Ticker]:
        return db.query(Ticker).filter(Ticker.symbol == symbol).first()


ticker = CRUDTicker(Ticker)

