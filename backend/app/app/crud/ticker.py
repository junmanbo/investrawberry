from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.ticker import Ticker
from app.schemas.ticker import TickerCreate, TickerUpdate


class CRUDTicker(CRUDBase[Ticker, TickerCreate, TickerUpdate]):
    def search_ticker_by_query(self, db: Session, *, query: str, skip: int = 0, limit: int = 10) -> List[Ticker]:
        return db.query(Ticker).filter(Ticker.ticker_knm.ilike(f"%{query}%")).offset(skip).limit(limit).all()



ticker = CRUDTicker(Ticker)

