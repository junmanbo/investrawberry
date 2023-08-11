import os
import time
import re
from coinmarketcapapi import CoinMarketCapAPI

from app.api import deps

from app import models, crud, schemas

from app.trading.upbit import Upbit
from app.trading.kis import KIS

db = next(deps.get_db())

# upbit 티커 정보 넣기
upbit = Upbit()
markets = upbit.get_market()

# Get the exchange ID for UPBIT
upbit_exchange = (
    db.query(models.Exchange).filter(models.Exchange.exchange_nm == "UPBIT").first()
)

# 저장할 코인들의 심볼 가져오기
saving_crypto_symbol = [
    market["base"]
    for market in markets
    if market["base"] != "Tokamak Network" and market["quote"] == "KRW"
]
cmc = CoinMarketCapAPI(api_key=os.getenv("CMC_KEY"))

rep = {}
prev_n = 0
next_n = 0
for i, market in enumerate(saving_crypto_symbol):
    next_n = 100 * (i + 1)
    n_symbols = saving_crypto_symbol[prev_n:next_n]

    if len(n_symbols) == 0:
        break

    tmp_rep = cmc.cryptocurrency_quotes_latest(
        symbol=",".join(n_symbols), convert="KRW"
    )
    rep.update(tmp_rep.data)
    prev_n = next_n
    time.sleep(1)

for market in markets:
    if market["quote"] == "KRW":
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

                ticker = crud.ticker.get_ticker_by_symbol(db=db, symbol=symbol)
                if ticker is None:
                    ticker_in = schemas.TickerCreate(
                        exchange_id=upbit_exchange.id,
                        asset_type="crypto",
                        symbol=market["base"],
                        currency=market["quote"],
                        ticker_knm=market["info"]["korean_name"],
                        maker_fee=market["maker"],
                        taker_fee=market["taker"],
                        marketcap=marketcap,
                        price=price,
                    )
                    # Add the new Ticker object to the database using the CRUD object
                    crud.ticker.create(db=db, obj_in=ticker_in)
                else:
                    ticker_in = schemas.TickerUpdate(marketcap=marketcap, price=price)
                    crud.ticker.update(db=db, db_obj=ticker, obj_in=ticker_in)
                print(
                    f"{symbol} - name: {market['info']['korean_name']} cap: {marketcap} price: {price}"
                )
db.commit()

# 국내주식 티커 정보 넣기
# My User ID
user = db.query(models.User).filter(models.User.email == "chchdelm3@icloud.com").first()

# Get the exchange ID for KIS
kis_exchange = (
    db.query(models.Exchange).filter(models.Exchange.exchange_nm == "KIS").first()
)

kis_exchange_key = (
    db.query(models.ExchangeKey)
    .filter(
        models.ExchangeKey.user_id == user.id,
        models.ExchangeKey.exchange_id == kis_exchange.id,
    )
    .first()
)

access_key = kis_exchange_key.access_key
secret_key = kis_exchange_key.secret_key
account = kis_exchange_key.account

kis = KIS(access_key, secret_key, account)
markets = kis.get_market()

markets.reset_index(drop=True, inplace=True)

for idx, row in markets.iterrows():
    ticker = crud.ticker.get_ticker_by_symbol(db=db, symbol=row["단축코드"])
    if ticker is None:
        ticker_in = schemas.TickerCreate(
            exchange_id=kis_exchange.id,
            asset_type="kr_stock",
            symbol=row["단축코드"],
            currency="KRW",
            ticker_knm=row["한글명"],
            marketcap=row["시가총액"],
            price=row["기준가"],
        )
        # Add the new Ticker object to the database using the CRUD object
        crud.ticker.create(db, obj_in=ticker_in)
    else:
        ticker_in = schemas.TickerUpdate(
            marketcap=row["시가총액"],
            price=row["기준가"],
        )
        crud.ticker.update(db=db, db_obj=ticker, obj_in=ticker_in)
    print(f"{row['단축코드']} - {row['한글명']} cap: {row['시가총액']} price: {row['기준가']}")
db.commit()

# Close the db
db.close()
