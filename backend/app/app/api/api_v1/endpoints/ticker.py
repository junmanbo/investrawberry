from typing import Any, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.Ticker])
async def search_ticker(
    keyword: str = Query(...),
    db: Session = Depends(deps.get_db),
    _: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    검색한 티커 목록 조회
    """

    tickers = crud.ticker.search_ticker_by_query(db=db, query=keyword)
    return tickers


@router.get("/top", response_model=List[schemas.Ticker])
async def search_ticker_top(
    db: Session = Depends(deps.get_db),
    _: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    시가총액 TOP3 종목
    """

    tickers = crud.ticker.search_ticker_by_marketcap(db=db)
    return tickers
