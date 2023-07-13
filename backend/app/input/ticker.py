import os

from app.db.session import SessionLocal
from app.crud.exchange import exchange
from app.crud.ticker import ticker
from app.schemas.ticker import TickerCreate
from app.trading.upbit import Upbit
from app.trading.kis import KIS


# Create a new session
session = SessionLocal()

# upbit 티커 정보 넣기
upbit = Upbit()
markets = upbit.get_market()
# Get the exchange ID for UPBIT
upbit_exchange_id = exchange.get_by_name(session, exchange_nm='UPBIT').id

# Iterate over the markets data and create new Ticker objects
for market in markets:
    print(market['id'])
    if market['quote'] == "KRW":
        ticker_data = TickerCreate(
            exchange_id=upbit_exchange_id,
            symbol=market['base'],
            currency=market['quote'],
            ticker_knm=market['info']['korean_name'],
            ticker_type=market['type'].upper(),
            is_coin=True,
            maker_fee=market['maker'],
            taker_fee=market['taker']
        )
        # Add the new Ticker object to the database using the CRUD object
        ticker.create(session, obj_in=ticker_data)

# 국내주식 티커 정보 넣기
access = os.getenv("KIS_ACCESS", "")
secret = os.getenv("KIS_SECRET", "")
acc = os.getenv("KIS_ACCOUNT", "")

kis = KIS(access, secret, acc)
markets = kis.get_market()

print(markets.head(5))

# Get the exchange ID for UPBIT
kis_exchange_id = exchange.get_by_name(session, exchange_nm='KIS').id

# Iterate over the markets data and create new Ticker objects
for index, row in markets.iterrows():
    print(row['한글명'])
    ticker_data = TickerCreate(
        exchange_id=kis_exchange_id,
        symbol=row['단축코드'],
        currency="KRW",
        ticker_knm=row['한글명'],
        ticker_type="SPOT",
        is_coin=False
    )
    # Add the new Ticker object to the database using the CRUD object
    ticker.create(session, obj_in=ticker_data)
# Close the session
session.close()


