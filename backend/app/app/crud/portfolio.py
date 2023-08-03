from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.portfolio import (
    Portfolio,
    PortfolioTicker,
    PortfolioTransaction,
)
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioUpdate,
    PortfolioTickerCreate,
    PortfolioTickerUpdate,
    PortfolioTransactionCreate,
    PortfolioTransactionUpdate,
)


class CRUDPortfolio(CRUDBase[Portfolio, PortfolioCreate, PortfolioUpdate]):
    def get_portfolio_by_user(
        self, db: Session, *, skip: int = 0, limit: int = 100, user_id: int
    ) -> List[Portfolio]:
        """유저가 저장한 포트폴리오 불러오기"""
        return (
            db.query(Portfolio)
            .offset(skip)
            .limit(limit)
            .filter(Portfolio.user_id == user_id)
            .all()
        )


portfolio = CRUDPortfolio(Portfolio)


class CRUDPortfolioTicker(
    CRUDBase[PortfolioTicker, PortfolioTickerCreate, PortfolioTickerUpdate]
):
    pass


portfolio_ticker = CRUDPortfolioTicker(PortfolioTicker)


class CRUDPortfolioTransaction(
    CRUDBase[
        PortfolioTransaction, PortfolioTransactionCreate, PortfolioTransactionUpdate
    ]
):
    pass


portfolio_transaction = CRUDPortfolioTransaction(PortfolioTransaction)
