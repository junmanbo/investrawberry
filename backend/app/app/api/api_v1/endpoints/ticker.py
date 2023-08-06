from typing import List, Dict, Any

from fastapi import APIRouter, Depends, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app.trading import kis, upbit

router = APIRouter()


@router.get("")
def search_ticker(
    keyword: str = Query(...),
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> List[Dict[str, Any]]:
    """
    검색한 티커 목록 조회
    """

    tickers = crud.ticker.search_ticker_by_query(db, query=keyword)
    result = []
    for ticker in tickers:
        ticker_data = jsonable_encoder(ticker)
        if ticker.asset_type.asset_nm == "STOCK":
            exchange_key = crud.exchange_key.get_key_by_owner_exchange(
                db, owner_id=current_user.id, exchange_id=ticker.exchange_id
            )
            client = kis.KIS(
                exchange_key.access_key, exchange_key.secret_key, exchange_key.account
            )
            ticker_data["current_price"] = client.get_price(ticker.symbol)
        elif ticker.asset_type.asset_nm == "CRYPTO":
            client = upbit.Upbit()
            ticker_data["current_price"] = client.get_price(
                ticker.symbol, ticker.currency
            )
        result.append(ticker_data)
    return result
