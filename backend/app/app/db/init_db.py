from sqlalchemy.orm import Session
from datetime import time

from app import crud, schemas
from app.core.config import settings

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly


def init_db(db: Session) -> None:
    # 관리자 계정 생성
    user = crud.user.get_by_email(db=db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = schemas.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            full_name=settings.FIRST_NAME,
            is_superuser=True,
            is_active=True,
            is_vip=True,
        )
        user = crud.user.create(db=db, obj_in=user_in)

    # 거래소 생성
    kis = crud.exchange.get_by_name(db=db, exchange_nm="KIS")
    if not kis:
        kis_in = schemas.ExchangeCreate(
            exchange_nm="KIS",
            exchange_knm="한국투자증권(국내)",
            open_time=time(hour=9, minute=0, second=0),
            close_time=time(hour=15, minute=30, second=0),
            is_summer=False,
            min_interval=1,
            min_amount=1,
            min_digit=0,
        )
        crud.exchange.create(db=db, obj_in=kis_in)

    upbit = crud.exchange.get_by_name(db=db, exchange_nm="UPBIT")
    if not upbit:
        upbit_in = schemas.ExchangeCreate(
            exchange_nm="UPBIT",
            exchange_knm="업비트",
            open_time=time(hour=9, minute=0, second=0),
            close_time=time(hour=8, minute=59, second=59),
            is_summer=False,
            min_interval=1,
            min_amount=10000,
            min_digit=6,
        )
        crud.exchange.create(db=db, obj_in=upbit_in)
