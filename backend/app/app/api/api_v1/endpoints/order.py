from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app import crud, models, schemas
from app.api import deps

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
