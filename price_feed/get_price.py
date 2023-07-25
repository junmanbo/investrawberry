# -*- coding: utf-8 -*-

from asyncio import run, gather
import ccxt.pro
import ccxt
import redis
import json
import mojito
import pprint



print('CCXT Version:', ccxt.__version__)


class UpbitData:
    def __init__(self) -> None:
        self.symbols = self.get_symbols()

    async def exchange_loop(self, exchange_id, symbols):
        exchange = getattr(ccxt.pro, exchange_id)()
        markets = await exchange.load_markets()
        await gather(*[self.watch_ticker_loop(exchange, symbol) for symbol in symbols])
        await exchange.close()


    async def watch_ticker_loop(self, exchange, symbol):
        # exchange.verbose = True  # uncomment for debugging purposes if necessary
        while True:
            try:
                ticker = await exchange.watch_ticker(symbol)
                now = exchange.milliseconds()
                print(exchange.iso8601(now), exchange.id, symbol, 'open:', ticker['open'], 'close:', ticker['close'])
                await self.put_data_in_redis(symbol, json.dumps(ticker))
            except Exception as e:
                print(str(e))
                # raise e  # uncomment to break all loops in case of an error in any one of them
                break  # you can break just this one loop if it fails

    async def put_data_in_redis(self, symbol, data):
        redis_client = redis.Redis(host="localhost", port=6379, db=0)
        key = symbol
        value = data
        redis_client.set(key, value)

    async def main(self):
        exchanges = {'upbit': self.symbols}
        loops = [self.exchange_loop(exchange_id, symbols) for exchange_id, symbols in exchanges.items()]
        await gather(*loops)

    def get_symbols(self):
        exchange = ccxt.upbit({})
        markets = exchange.fetch_markets()
        symbols = [market["symbol"] for market in markets if market["symbol"].split("/")[1] == "KRW"]
        return symbols


class KISData:
    def __init__(self, key, secret) -> None:
        self.broker_ws = mojito.KoreaInvestmentWS(key, secret, ["H0STCNT0", "H0STASP0"], ["005930", "000660"])
        self.broker_ws.start()

    async def watch_data_loop(self):
        while True:
            try:
                print("kis data")
                data_ = self.broker_ws.get()
                if data_[0] == '체결':
                    print(data_[1])
                elif data_[0] == '호가':
                    print(data_[1])
                elif data_[0] == '체잔':
                    print(data_[1])
            except Exception as e:
                print(str(e))
                break

    async def main(self):
        await self.watch_data_loop()


if __name__ == "__main__":
    # upbit = UpbitData()
    # run(upbit.main())

    kis = KISData(key, secret)
    run(kis.main())
