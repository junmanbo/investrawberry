from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.trading import upbit, kis

router = APIRouter()


@router.post("/simple", response_model=schemas.SimpleTransaction)
def simple_order(
    db: Session = Depends(deps.get_db),
    order: schemas.SimpleTransactionCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    단순 주문(market, limit)
    """
    ticker = crud.ticker.get(order.ticker_id)
    exchange = crud.exchange.get(ticker.exchange_id)
    order_type = crud.order_type.get(order.order_type_id)
    order.order_type = order_type.order_type_nm

    key = crud.exchange_key.get_key_by_owner_exchange(db, owner_id=current_user.id, exchange_id=exchange.id)

    if exchange.exchange_nm == "UPBIT":
        client = upbit.Upbit(key.access_key, key.secret_key)
    elif exchange.exchange_nm == "KIS":
        client = kis.KIS(key.access_key, key.secret_key, key.account)

    order_result = client.place_order(order)




            
    return order_result
