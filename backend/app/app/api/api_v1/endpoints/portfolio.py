from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("", response_model=schemas.Portfolio)
def get_portfolio(
    portfolio_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    저장한 포트폴리오 가져오기
    """
    portfolio = crud.portfolio.get(db=db, id=portfolio_id)
    return portfolio


@router.post("", response_model=schemas.Portfolio)
def create_portfolio(
    pf_data: Dict,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    포트폴리오 구성 생성
    pf_data: 포트폴리오 구성 + 티커 데이터
    """
    portfolio = schemas.PortfolioCreate
    portfolio_ticker = schemas.PortfolioTickerCreate

    # portfolio 기본 정보 입력
    pf_input = pf_data["portfolio"]
    portfolio.user_id = current_user.id
    portfolio.rebal_period = pf_input.get("rebal_period", None)
    portfolio.is_running = pf_input.get("is_running", None)
    portfolio.amount = pf_input.get("amount", None)
    portfolio.memo = pf_input.get("memo", None)
    portfolio = crud.portfolio.create(db=db, obj_in=portfolio)

    # 포트폴리오의 티커 구성 입력
    tickers = pf_data["tickers"]
    for ticker in tickers:
        portfolio_ticker.portfolio_id = portfolio.id
        portfolio_ticker.ticker_id = ticker["ticker_id"]
        portfolio_ticker.weight = ticker["weight"]
        portfolio_ticker = crud.portfolio_ticker.create(db=db, obj_in=portfolio_ticker)

    return portfolio
