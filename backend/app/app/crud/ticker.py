from typing import List

from sqlalchemy.orm import Session, aliased
from sqlalchemy import func

from app.crud.base import CRUDBase
from app.models.ticker import Ticker
from app.schemas.ticker import TickerCreate, TickerUpdate


class CRUDTicker(CRUDBase[Ticker, TickerCreate, TickerUpdate]):
    def search_ticker_by_query(
        self, db: Session, *, query: str, skip: int = 0, limit: int = 5
    ) -> List[Ticker]:
        return (
            db.query(Ticker)
            .filter(Ticker.ticker_knm.ilike(f"%{query}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_ticker_by_marketcap(self, db: Session) -> List[Ticker]:
        subq = db.query(
            Ticker.exchange_id,
            func.row_number()
            .over(partition_by=Ticker.exchange_id, order_by=Ticker.marketcap.desc())
            .label("row_num"),
            Ticker,
        ).subquery()
        aliased_ticker = aliased(Ticker, subq)
        results = db.query(aliased_ticker).filter(subq.c.row_num <= 3).all()

        return results

    def get_ticker_by_symbol(self, db: Session, symbol: str) -> Ticker | None:
        return db.query(Ticker).filter_by(symbol=symbol).first()


ticker = CRUDTicker(Ticker)
