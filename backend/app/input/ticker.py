from app.db.session import SessionLocal

from app.crud.exchange import exchange
from app.crud.exchange_key import exchange_key
from app.crud.ticker import ticker
from app.crud.asset_type import asset_type

from app.schemas.ticker import TickerCreate
from app.trading.upbit import Upbit
from app.trading.kis import KIS


# # Create a new session
session = SessionLocal()

# upbit 티커 정보 넣기
upbit = Upbit()
markets = upbit.get_market()
# Get the exchange ID for UPBIT
upbit_exchange_id = exchange.get_by_name(session, exchange_nm="UPBIT").id
crypto_asset_id = asset_type.get_by_name(session, asset_nm="CRYPTO").id

# Iterate over the markets data and create new Ticker objects
for market in markets:
    print(market['id'])
    if market['quote'] == "KRW":
        ticker_data = TickerCreate(
            exchange_id=upbit_exchange_id,
            asset_type_id=crypto_asset_id,
            symbol=market['base'],
            currency=market['quote'],
            ticker_knm=market['info']['korean_name'],
            maker_fee=market['maker'],
            taker_fee=market['taker']
        )
        # Add the new Ticker object to the database using the CRUD object
        ticker.create(session, obj_in=ticker_data)

# 국내주식 티커 정보 넣기
# Get the exchange ID for KIS
kis_exchange_id = exchange.get_by_name(session, exchange_nm='KIS').id
kis_exchange_key = exchange_key.get_key_by_owner_exchange(session, owner_id=1, exchange_id=kis_exchange_id)
stock_asset_id = asset_type.get_by_name(session, asset_nm="STOCK").id

access_key = kis_exchange_key.access_key
secret_key = kis_exchange_key.secret_key
account = kis_exchange_key.account

kis = KIS(access_key, secret_key, account)
markets = kis.get_market()

print(markets.head(5))


# Iterate over the markets data and create new Ticker objects
for index, row in markets.iterrows():
    print(row['한글명'])
    ticker_data = TickerCreate(
        exchange_id=kis_exchange_id,
        asset_type_id=stock_asset_id,
        symbol=row['단축코드'],
        currency="KRW",
        ticker_knm=row['한글명'],
    )
    # Add the new Ticker object to the database using the CRUD object
    ticker.create(session, obj_in=ticker_data)
# Close the session
session.close()


