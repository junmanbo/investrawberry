from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app import crud, models, schemas
from app.api import deps
from app import EXCHANGE_CLASSES

router = APIRouter()


@router.get("/simple/transactions", response_model=List[schemas.Transaction])
async def get_transactions(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    진행 중인 주문 내역 가져오기
    """
    transactions = crud.transaction.get_open_transactions(
        db=db, user_id=current_user.id
    )
    return transactions


@router.post("/simple", response_model=schemas.Transaction)
async def simple_order(
    order: schemas.TransactionCreate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    단순 주문(market, limit)
    """
    order.user_id = current_user.id
    transaction = crud.transaction.create(db=db, obj_in=order)
    celery_app.send_task("app.worker.place_order", args=[transaction.id])
    return transaction


@router.put("/simple/cancel", response_model=schemas.Transaction)
async def cancel_order(
    transaction_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    미체결 지정가 주문 취소
    """
    transaction = crud.transaction.get(db=db, id=transaction_id)
    if transaction is None:
        raise HTTPException(status_code=400, detail="Transaction is not found.")
    exchange = transaction.ticker.exchange

    key = crud.exchange_key.get_key_by_owner_exchange(
        db, owner_id=current_user.id, exchange_id=exchange.id
    )

    exchange_nm = key.exchange.exchange_nm
    if exchange_nm in EXCHANGE_CLASSES:
        client_class = EXCHANGE_CLASSES[exchange_nm]
        client = client_class(key.access_key, key.secret_key, key.account)
    else:
        raise HTTPException(status_code=404, detail="Exchange is not found.")

    # 주문 취소
    client.cancel_order(transaction.uuid)

    # 취소된 매매내역 상태 업데이트
    transaction_in = schemas.TransactionUpdate(uuid=transaction.uuid, status="cancel")
    transaction = crud.transaction.update(
        db=db, db_obj=transaction, obj_in=transaction_in
    )

    return transaction
