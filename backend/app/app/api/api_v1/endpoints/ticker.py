from typing import List, Dict, Any

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app import trading

router = APIRouter()


async def add_current_price(db: Session, current_user, result, tickers):
    for ticker in tickers:
        ticker_data = jsonable_encoder(ticker)
        exchange_nm = ticker.exchange.exchange_nm

        if ticker.asset_type == "kr_stock":
            key = crud.exchange_key.get_key_by_owner_exchange(
                db, owner_id=current_user.id, exchange_id=ticker.exchange_id
            )
        else:
            key = None
        client = trading.get_client(exchange_nm=exchange_nm, key=key)
        if not client:
            raise HTTPException(status_code=404, detail="Exchange not found")
        ticker_data["current_price"] = client.get_price(ticker.symbol)
        result.append(ticker_data)
    return result


@router.get("")
async def search_ticker(
    keyword: str = Query(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> List[Dict[str, Any]]:
    """
    검색한 티커 목록 조회
    """

    tickers = crud.ticker.search_ticker_by_query(db=db, query=keyword)
    result = []
    current_user = crud.user.get_by_email(db=db, email="chchdelm3@icloud.com")
    result = await add_current_price(db, current_user, result, tickers)
    return result


@router.get("/top")
async def search_ticker_top(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> List[Dict[str, Any]]:
    """
    시가총액 TOP3 종목
    """

    tickers = crud.ticker.search_ticker_by_marketcap(db=db)
    result = []
    current_user = crud.user.get_by_email(db=db, email="chchdelm3@icloud.com")
    result = await add_current_price(db, current_user, result, tickers)
    return result
