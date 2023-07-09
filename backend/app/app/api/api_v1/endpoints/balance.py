from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.trading import upbit

router = APIRouter()


@router.get("")
def get_balance_all(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    계좌 자산 전체 조회
    """
    exchange_keys = crud.exchange_key.get_multi_by_owner(db, owner_id=current_user.id)
    total_balance = {}
    for key in exchange_keys:
        if key.exchange.exchange_nm == "UPBIT":
            client = upbit.Upbit(key.access_key, key.secret_key)
        elif key.exchange.exchange_nm == "KIS":
            continue
        balance = client.get_total_balance()
        total_balance[key.exchange.exchange_nm] = balance
            
    return total_balance
