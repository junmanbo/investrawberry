from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models
from app.api import deps
from app import EXCHANGE_CLASSES

router = APIRouter()


@router.get("")
async def get_balance_all(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    계좌 자산 전체 조회
    """
    exchange_keys = crud.exchange_key.get_multi_by_owner(db, owner_id=current_user.id)
    total_balance = {}
    for key in exchange_keys:
        exchange_nm = key.exchange.exchange_nm
        if exchange_nm in EXCHANGE_CLASSES:
            client_class = EXCHANGE_CLASSES[exchange_nm]
            client = client_class(key.access_key, key.secret_key, key.account)
            balance = client.get_total_balance()
            total_balance[exchange_nm] = balance
        else:
            raise HTTPException(status_code=404, detail="Exchange is not found.")

        balance = client.get_total_balance()
        total_balance[key.exchange.exchange_nm] = balance

    return total_balance
