from typing import Any, Dict

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app import crud, models, schemas
from app.api import deps
from app.trading import upbit, kis

router = APIRouter()


@router.get("", response_model=schemas.Portfolio)
def get_portfolio(
    portfolio_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    저장한 포트폴리오 가져오기
    """
    portfolio = crud.portfolio.get(db=db, id=portfolio_id)
    return portfolio


@router.post("", response_model=schemas.Portfolio)
def create_portfolio(
    ticker_weight: Dict[int, int],
    rebal_period: int,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    포트폴리오 구성 생성
    """
    portfolio = schemas.PortfolioCreate
    portfolio.user_id = current_user.id
    portfolio.rebal_period = rebal_period
    for ticker_id, weight in ticker_weight.items():
        portfolio.ticker_id = ticker_id
        portfolio.weight = weight
        portfolio = crud.portfolio.create(db=db, obj_in=portfolio)

    return portfolio


@router.put("", response_model=schemas.Portfolio)
def update_portfolio(
    portfolio: schemas.PortfolioUpdate,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    포트폴리오 구성 수정
    """
    st = crud.simple_transaction.get(db=db, id=st_id)
    exchange = st.ticker.exchange
    key = crud.exchange_key.get_key_by_owner_exchange(
        db, owner_id=current_user.id, exchange_id=exchange.id
    )

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
