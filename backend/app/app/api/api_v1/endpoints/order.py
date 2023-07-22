from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app import crud, models, schemas
from app.api import deps
from app.trading import upbit, kis

router = APIRouter()


@router.post("/simple", response_model=schemas.SimpleTransaction)
def simple_order(
    order: schemas.SimpleTransactionCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    단순 주문(market, limit)
    """
    order.user_id = current_user.id
    simple_transaction = crud.simple_transaction.create(db=db, obj_in=order)
    celery_app.send_task("app.worker.place_order", args=[simple_transaction.id])
    return simple_transaction

@router.put("/simple/cancel", response_model=schemas.SimpleTransaction)
def cancel_order(
    st_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    미체결 지정가 주문 취소
    """
    st = crud.simple_transaction.get(db=db, id=st_id)
    exchange = st.ticker.exchange
    key = crud.exchange_key.get_key_by_owner_exchange(db, owner_id=current_user.id, exchange_id=exchange.id)

    if exchange.exchange_nm == "UPBIT":
        client = upbit.Upbit(key.access_key, key.secret_key)
    elif exchange.exchange_nm == "KIS":
        client = kis.KIS(key.access_key, key.secret_key, key.account)

    # 주문 취소
    client.cancel_order(st.uuid)

    # 취소된 매매내역 상태 업데이트
    st_in = schemas.SimpleTransactionUpdate(uuid=st.uuid, status="cancel")
    st = crud.simple_transaction.update(db=db, db_obj=st, obj_in=st_in)

    return st
