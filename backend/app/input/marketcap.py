from coinmarketcapapi import CoinMarketCapAPI
from pprint import pprint

cmc = CoinMarketCapAPI(api_key="ec4cc4ef-c9da-474a-82a1-9b7c412466d8")

symbols = ['BTC', 'ETH', 'LINK', 'SOL']
rep = cmc.cryptocurrency_quotes_latest(symbol=','.join(symbols), convert="KRW")

for symbol, data in rep.data.items():
    crypto = data[0]
    marketcap = int(crypto["quote"]["KRW"]["market_cap"])
    marketcap = marketcap // 100000000
    price = int(crypto["quote"]["KRW"]["price"])
    print(f"{symbol}: cap: {marketcap} price: {price}")

