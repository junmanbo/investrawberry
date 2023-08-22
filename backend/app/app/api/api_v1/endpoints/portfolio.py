from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("", response_model=schemas.Portfolio)
async def get_portfolio(
    portfolio_id: int = Query(...),
    db: Session = Depends(deps.get_db),
    _: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    저장한 포트폴리오 가져오기
    """
    portfolio = crud.portfolio.get(db=db, id=portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


@router.get("/all", response_model=List[schemas.Portfolio])
async def get_portfolios_by_user(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    유저가 저장한 포트폴리오 전부 가져오기
    """
    portfolios = crud.portfolio.get_portfolio_by_user(db=db, user_id=current_user.id)
    if not portfolios:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolios


@router.post("", response_model=schemas.Portfolio)
async def create_portfolio(
    pf_data: Dict,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    포트폴리오 구성 생성
    pf_data: 포트폴리오 구성 + 티커 데이터
    """
    # portfolio 기본 정보 입력
    portfolio_in = schemas.PortfolioCreate(
        user_id=current_user.id,
        rebal_period=pf_data.get("rebal_period", None),
        is_running=pf_data.get("is_running", None),
        amount=pf_data.get("amount", None),
        memo=pf_data.get("memo", None),
    )
    portfolio = crud.portfolio.create(db=db, obj_in=portfolio_in)

    # 포트폴리오의 티커 구성 입력
    pt_data = pf_data["portfolio_ticker"]
    for portfolio_ticker in pt_data:
        portfolio_ticker_in = schemas.PortfolioTickerCreate(
            portfolio_id=portfolio.id,
            ticker_id=portfolio_ticker["ticker_id"],
            weight=portfolio_ticker["weight"],
        )
        crud.portfolio_ticker.create(db=db, obj_in=portfolio_ticker_in)

    portfolio = crud.portfolio.get(db=db, id=portfolio.id)
    if not portfolio:
        raise HTTPException(status_code=400, detail="Failed creating portfolio")

    return portfolio


@router.put("", response_model=schemas.Portfolio)
async def update_portfolio(
    pf_data: Dict,
    db: Session = Depends(deps.get_db),
    _: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    포트폴리오 구성 업데이트
    pf_data: 포트폴리오 구성 + 티커 데이터
    """
    portfolio = crud.portfolio.get(db=db, id=pf_data["id"])
    if portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio is not found.")

    # portfolio 기본 정보 업데이트
    portfolio_in = schemas.PortfolioUpdate(
        rebal_period=pf_data.get("rebal_period", portfolio.rebal_period),
        is_running=pf_data.get("is_running", portfolio.is_running),
        amount=pf_data.get("amount", portfolio.amount),
        memo=pf_data.get("memo", portfolio.memo),
    )
    portfolio = crud.portfolio.update(db=db, db_obj=portfolio, obj_in=portfolio_in)

    # 포트폴리오의 티커
    pt_datas = pf_data["portfolio_ticker"]

    current_tickers = set(ticker.ticker_id for ticker in portfolio.portfolio_ticker)
    new_tickers = set(pt_data["ticker_id"] for pt_data in pt_datas)

    del_tickers = current_tickers - new_tickers  # 삭제할 티커
    cre_tickers = new_tickers - current_tickers  # 새로 추가할 티커
    upd_tickers = current_tickers & new_tickers  # 기존 티커 업데이트

    for del_ticker in del_tickers:
        portfolio_ticker = crud.portfolio_ticker.get_by_portfolio_ticker(
            db=db, portfolio_id=portfolio.id, ticker_id=del_ticker
        )
        crud.portfolio_ticker.remove(db=db, id=portfolio_ticker.id)

    for upd_ticker in upd_tickers:
        for pt_data in pt_datas:
            if pt_data["ticker_id"] == upd_ticker:
                portfolio_ticker = crud.portfolio_ticker.get_by_portfolio_ticker(
                    db=db, portfolio_id=portfolio.id, ticker_id=upd_ticker
                )
                portfolio_ticker_in = schemas.PortfolioTickerUpdate(
                    weight=pt_data.get("weight", None)
                )
                crud.portfolio_ticker.update(
                    db=db, db_obj=portfolio_ticker, obj_in=portfolio_ticker_in
                )

    for cre_ticker in cre_tickers:
        for pt_data in pt_datas:
            if pt_data["ticker_id"] == cre_ticker:
                portfolio_ticker_in = schemas.PortfolioTickerCreate(
                    portfolio_id=portfolio.id,
                    ticker_id=pt_data.get("ticker_id", None),
                    weight=pt_data.get("weight", None),
                )
                crud.portfolio_ticker.create(db=db, obj_in=portfolio_ticker_in)

    portfolio = crud.portfolio.get(db=db, id=portfolio.id)
    return portfolio
