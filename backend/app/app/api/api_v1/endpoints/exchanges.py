from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.get("", response_model=List[schemas.Exchange])
async def read_exchanges(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    _: models.User = Depends(deps.get_current_active_user),
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
    _: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create new exchange.
    """
    exchange = crud.exchange.create(db, obj_in=exchange_in)
    return exchange


@router.put("/{exchange_id}", response_model=schemas.Exchange)
async def update_exchange(
    exchange_id: int,
    exchange_in: schemas.ExchangeUpdate,
    _: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
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
    _: models.User = Depends(deps.get_current_active_user),
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
