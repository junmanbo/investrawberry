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
upbit_exchange = db.query(models.Exchange).filter(models.Exchange.exchange_nm=="UPBIT").first()
upbit_exchange_id = upbit_exchange.id

asset_type_crypto = db.query(models.AssetType).filter(models.AssetType.asset_nm=="CRYPTO").first()
crypto_asset_id = asset_type_crypto.id

# 현재 저장된 코인들의 심볼 가져오기
cryptos = db.query(models.Ticker).filter(models.Ticker.asset_type_id==crypto_asset_id).all()
saved_crypto_symbol = [crypto.symbol for crypto in cryptos]

# 저장할 코인들의 심볼 가져오기
saving_crypto_symbol = [market["base"] for market in markets if market["base"] != "Tokamak Network" and market["quote"] == "KRW"]

# 삭제할 코인들의 심볼 찾기
delete_crypto_symbol = set(saved_crypto_symbol) - set(saving_crypto_symbol)
print(f"삭제할 코인 리스트: {delete_crypto_symbol}")

# 삭제할 코인들 삭제하기
for symbol in delete_crypto_symbol:
    db.query(models.Ticker).filter(models.Ticker.symbol==symbol).delete()
db.commit()

# 추가할 코인들의 심볼 찾기
create_crypto_symbol = list(set(saving_crypto_symbol) - set(saved_crypto_symbol))

cmc = CoinMarketCapAPI(api_key=os.getenv("CMC_KEY"))

rep = {}
i = 1
prev_n = 0
next_n = 0
while next_n < len(create_crypto_symbol):
    next_n = 100 * i
    n_symbols = create_crypto_symbol[prev_n:next_n]

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

                ticker_data = schemas.TickerCreate(
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
                crud.ticker.create(db, obj_in=ticker_data)
                print(f"{symbol} - name: {market['info']['korean_name']} \
                cap: {marketcap} price: {price}")
db.commit()

# 국내주식 티커 정보 넣기
# My User ID
user = db.query(models.User).filter(models.User.email=="chchdelm3@icloud.com").first()
user_id = user.id

# Get the exchange ID for KIS
kis_exchange = db.query(models.Exchange).filter(models.Exchange.exchange_nm=="KIS").first()
kis_exchange_id = kis_exchange.id

kis_exchange_key = db.query(models.ExchangeKey).filter(models.ExchangeKey.user_id==user_id,
                                                       models.ExchangeKey.exchange_id==kis_exchange_id).first()
stock_asset_type = db.query(models.AssetType).filter(models.AssetType.asset_nm=="STOCK").first()
stock_asset_id = stock_asset_type.id

access_key = kis_exchange_key.access_key
secret_key = kis_exchange_key.secret_key
account = kis_exchange_key.account

kis = KIS(access_key, secret_key, account)
markets = kis.get_market()

markets.reset_index(drop=True, inplace=True)

# 현재 저장된 주식들의 심볼 가져오기
stocks = db.query(models.Ticker).filter(models.Ticker.asset_type_id==stock_asset_id).all()
saved_stock_symbol = [stock.symbol for stock in stocks]

# 저장할 주식들의 심볼 가져오기
saving_stock_symbol = [row["단축코드"] for _, row in markets.iterrows() if re.match(r'^\d', row['단축코드'])]

# 삭제할 주식들의 심볼 찾기
delete_stock_symbol = set(saved_stock_symbol) - set(saving_stock_symbol)
print(f"삭제할 주식 리스트: {delete_stock_symbol}")

# 삭제할 주식들 삭제하기
for symbol in delete_stock_symbol:
    db.query(models.Ticker).filter(models.Ticker.symbol==symbol).delete()
db.commit()

# 추가할 주식들의 심볼 찾기
create_stock_symbol = set(saving_stock_symbol) - set(saved_stock_symbol)

# 추가할 주식들 추가하기
for symbol in create_stock_symbol:
    row = markets.loc[markets['단축코드'] == symbol].iloc[0]
    ticker_data = schemas.TickerCreate(
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
    crud.ticker.create(db, obj_in=ticker_data)
db.commit()

# Close the db
db.close()
