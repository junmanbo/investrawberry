from typing import List
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.portfolio import (
    Portfolio,
    PortfolioTicker,
)
from app.schemas.portfolio import (
    PortfolioCreate,
    PortfolioUpdate,
    PortfolioTickerCreate,
    PortfolioTickerUpdate,
)


class CRUDPortfolio(CRUDBase[Portfolio, PortfolioCreate, PortfolioUpdate]):
    def get_portfolio_by_user(self, db: Session, *, user_id: int) -> List[Portfolio]:
        """유저가 저장한 포트폴리오 조회"""
        return db.query(Portfolio).filter(Portfolio.user_id == user_id).all()

    def get_portfolio_running(
        self, db: Session, *, is_running: bool
    ) -> List[Portfolio]:
        """실행중인 포트폴리오 조회"""
        return db.query(Portfolio).filter_by(is_running=is_running).all()


portfolio = CRUDPortfolio(Portfolio)


class CRUDPortfolioTicker(
    CRUDBase[PortfolioTicker, PortfolioTickerCreate, PortfolioTickerUpdate]
):
    def get_by_portfolio_ticker(
        self, db: Session, *, portfolio_id: int, ticker_id: int
    ) -> PortfolioTicker:
        """포트폴리오 id와 ticker id로 조회"""
        return (
            db.query(PortfolioTicker)
            .filter_by(portfolio_id=portfolio_id, ticker_id=ticker_id)
            .first()
        )

    def get_by_portfolio_id(
        self, db: Session, *, portfolio_id: int
    ) -> List[PortfolioTicker]:
        """포트폴리오 id로 조회"""
        return db.query(PortfolioTicker).filter_by(portfolio_id=portfolio_id).all()


portfolio_ticker = CRUDPortfolioTicker(PortfolioTicker)
