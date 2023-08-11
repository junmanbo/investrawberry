from datetime import time
from app.db.session import SessionLocal
from app.crud.exchange import exchange
from app.schemas.exchange import ExchangeCreate

# Create a new session
session = SessionLocal()

# Create new Exchange objects
exchange1 = ExchangeCreate(
    exchange_nm="KIS",
    exchange_knm="한국투자증권(국내)",
    open_time=time(hour=9, minute=0, second=0),
    close_time=time(hour=15, minute=30, second=0),
    is_summer=False,
    min_interval=1,
    min_amount=1,
    min_digit=0,
)

exchange2 = ExchangeCreate(
    exchange_nm="UPBIT",
    exchange_knm="업비트",
    open_time=time(hour=9, minute=0, second=0),
    close_time=time(hour=8, minute=59, second=59),
    is_summer=False,
    min_interval=1,
    min_amount=10000,
    min_digit=6,
)

# Add the new objects to the database using the CRUD object
exchange.create(session, obj_in=exchange1)
print(f"{exchange1} 추가")
exchange.create(session, obj_in=exchange2)
print(f"{exchange2} 추가")

# Close the session
session.close()
