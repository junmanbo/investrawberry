import os
import time
from coinmarketcapapi import CoinMarketCapAPI

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
symbols = []
for market in markets:
    if market['base'] == "Tokamak Network":
        continue
    elif market['quote'] == "KRW":
        symbols.append(market["base"])

cmc = CoinMarketCapAPI(api_key=os.getenv("CMC_KEY"))

rep = {}
i = 1
prev_n = 0
next_n = 0
while next_n < len(symbols):
    next_n = 100 * i
    n_symbols = symbols[prev_n:next_n]

    tmp_rep = cmc.cryptocurrency_quotes_latest(symbol=','.join(n_symbols), convert="KRW")
    rep.update(tmp_rep.data)
    prev_n = next_n
    i += 1
    time.sleep(1)

for market in markets:
    if market['quote'] == "KRW":
        for symbol, data in rep.items():
            if symbol == market["base"]:
                try:
                    crypto = data[0]
                except IndexError as e:
                    print(e)
                    continue
                marketcap = int(crypto["quote"]["KRW"]["market_cap"])
                marketcap = marketcap // 100000000
                price = int(crypto["quote"]["KRW"]["price"])

                ticker_data = TickerCreate(
                    exchange_id=upbit_exchange_id,
                    asset_type_id=crypto_asset_id,
                    symbol=market['base'],
                    currency=market['quote'],
                    ticker_knm=market['info']['korean_name'],
                    maker_fee=market['maker'],
                    taker_fee=market['taker'],
                    marketcap=marketcap,
                    price=price,
                )
                # Add the new Ticker object to the database using the CRUD object
                ticker.create(session, obj_in=ticker_data)
                print(f"{symbol} - name: {market['info']['korean_name']} \
                cap: {marketcap} price: {price}")


# 국내주식 티커 정보 넣기
# Get the exchange ID for KIS
kis_exchange_id = exchange.get_by_name(session, exchange_nm='KIS').id
kis_exchange_key = exchange_key.get_key_by_owner_exchange(session, owner_id=2, exchange_id=kis_exchange_id)
stock_asset_id = asset_type.get_by_name(session, asset_nm="STOCK").id

access_key = kis_exchange_key.access_key
secret_key = kis_exchange_key.secret_key
account = kis_exchange_key.account

kis = KIS(access_key, secret_key, account)
markets = kis.get_market()

markets.reset_index(drop=True, inplace=True)

# Iterate over the markets data and create new Ticker objects
for index, row in markets.iterrows():
    ticker_data = TickerCreate(
        exchange_id=kis_exchange_id,
        asset_type_id=stock_asset_id,
        symbol=row['단축코드'],
        currency="KRW",
        ticker_knm=row['한글명'],
        marketcap=row['시가총액'],
        price=row['기준가']
    )
    print(f"{row['단축코드']} - {row['한글명']} cap: {row['시가총액']} price: {row['기준가']}")
    # Add the new Ticker object to the database using the CRUD object
    ticker.create(session, obj_in=ticker_data)

# Close the session
session.close()
