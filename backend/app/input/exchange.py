from datetime import time
from app.db.session import SessionLocal
from app.crud.exchange import exchange
from app.schemas.exchange import ExchangeCreate

# Create a new session
session = SessionLocal()

# Create new Exchange objects
exchange1 = ExchangeCreate(
    exchange_nm='KIS',
    exchange_knm='한국투자증권(국내)',
    open_time=time(hour=9, minute=0, second=0),
    close_time=time(hour=15, minute=30, second=0),
    min_interval=1,
    min_amount=1,
    is_summer=False,
    is_coin=False
)

exchange2 = ExchangeCreate(
    exchange_nm='UPBIT',
    exchange_knm='업비트',
    open_time=time(hour=9, minute=0, second=0),
    close_time=time(hour=8, minute=59, second=59),
    min_interval=1,
    min_amount=10000,
    is_summer=False,
    is_coin=True
)

exchange3 = ExchangeCreate(
    exchange_nm='KIS_INTL',
    exchange_knm='한국투자증권(해외)',
    open_time=time(hour=23, minute=30, second=0),
    close_time=time(hour=6, minute=0, second=0),
    min_interval=1,
    min_amount=1,
    is_summer=True,
    is_coin=False
)

# Add the new objects to the database using the CRUD object
exchange.create(session, obj_in=exchange1)
exchange.create(session, obj_in=exchange2)
exchange.create(session, obj_in=exchange3)

# Close the session
session.close()

