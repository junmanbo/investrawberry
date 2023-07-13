from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.ExchangeKey])
def read_exchange_keys(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve exchange keys.
    """
    exchange_keys = crud.exchange_key.get_multi_by_owner(db, owner_id=current_user.id)
    return exchange_keys


@router.post("", response_model=schemas.ExchangeKey)
def create_exchange_key(
    *,
    db: Session = Depends(deps.get_db),
    exchange_nm: str = Body(None),
    exchange_key_in: schemas.ExchangeKeyCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new exchange key.
    """
    exchange = crud.exchange.get_by_name(db, exchange_nm=exchange_nm)
    if exchange is None:
        raise HTTPException(
            status_code=404,
            detail="The exchange with this name does not exist in the system",
        )
    exchange_key_in.exchange_id = exchange.id
    exchange_key_in.user_id = current_user.id
    exchange_key = crud.exchange_key.create(db, obj_in=exchange_key_in)
    return exchange_key


@router.put("/{exchange_key_id}", response_model=schemas.ExchangeKey)
def update_exchange_key(
    *,
    db: Session = Depends(deps.get_db),
    exchange_key_id: int,
    exchange_key_in: schemas.ExchangeKeyUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update an exchange key.
    """
    exchange_key = crud.exchange_key.get(db, id=exchange_key_id)
    if not exchange_key:
        raise HTTPException(
            status_code=404,
            detail="The exchange key with this id does not exist in the system",
        )
    if exchange_key.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    exchange_key = crud.exchange_key.update(
        db, db_obj=exchange_key, obj_in=exchange_key_in
    )
    return exchange_key


@router.delete("/{exchange_key_id}")
def delete_exchange_key(
    *,
    db: Session = Depends(deps.get_db),
    exchange_key_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete an exchange key.
    """
    exchange_key = crud.exchange_key.get(db, id=exchange_key_id)
    if not exchange_key:
        raise HTTPException(
            status_code=404,
            detail="The exchange key with this id does not exist in the system",
        )
    if exchange_key.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    exchange_key = crud.exchange_key.remove(db, id=exchange_key_id)
    if exchange_key is True:
        return {"message": "success"}
    else:
        return {"message": "failed"}
