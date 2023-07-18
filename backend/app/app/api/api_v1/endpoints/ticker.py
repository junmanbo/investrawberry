from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps

router = APIRouter()


@router.get("")
def search_ticker(
    keyword: str = Query(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    검색한 티커 목록 조회
    """

    tickers = crud.ticker.search_ticker_by_query(db, query=keyword)
    return tickers

