from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.Exchange])
async def read_exchanges(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Retrieve exchanges.
    """
    exchanges = crud.exchange.get_multi(db, skip=skip, limit=limit)
    return exchanges


@router.post("", response_model=schemas.Exchange)
async def create_exchange(
    *,
    db: Session = Depends(deps.get_db),
    exchange_in: schemas.ExchangeCreate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new exchange.
    """
    exchange = crud.exchange.create(db, obj_in=exchange_in)
    return exchange


@router.put("/{exchange_id}", response_model=schemas.Exchange)
async def update_exchange(
    *,
    db: Session = Depends(deps.get_db),
    exchange_id: int,
    exchange_in: schemas.ExchangeUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update an exchange.
    """
    exchange = crud.exchange.get(db, id=exchange_id)
    if not exchange:
        raise HTTPException(
            status_code=404,
            detail="The exchange with this id does not exist in the system",
        )
    exchange = crud.exchange.update(db, db_obj=exchange, obj_in=exchange_in)
    return exchange


@router.get("/{exchange_id}", response_model=schemas.Exchange)
async def read_exchange(
    exchange_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Get a specific exchange by id.
    """
    exchange = crud.exchange.get(db, id=exchange_id)
    if not exchange:
        raise HTTPException(
            status_code=404,
            detail="The exchange with this id does not exist in the system",
        )
    return exchange
