from asyncio import run, gather
import ccxt.pro
import ccxt
import redis
import json
import mojito
import os
import re

from typing import List

print("CCXT Version:", ccxt.__version__)

REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", "localhost")


class UpbitData:
    def __init__(self) -> None:
        self.symbols = self.get_symbols()
        self.redis_client = redis.Redis(host=REDIS_HOSTNAME, port=6379, db=0)

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
                await self.put_data_in_redis(symbol, json.dumps(ticker))
            except Exception as e:
                print(str(e))
                # raise e  # uncomment to break all loops in case of an error in any one of them
                break  # you can break just this one loop if it fails

    async def put_data_in_redis(self, symbol, data):
        key = symbol
        value = data
        self.redis_client.set(key, value)

    async def main(self):
        exchanges = {"upbit": self.symbols}
        loops = [
            self.exchange_loop(exchange_id, symbols)
            for exchange_id, symbols in exchanges.items()
        ]
        await gather(*loops)

    def get_symbols(self):
        exchange = ccxt.upbit({})
        markets = exchange.fetch_markets()
        symbols = [
            market["symbol"]
            for market in markets
            if market["symbol"].split("/")[1] == "KRW"
        ]
        return symbols


class KISData:
    def __init__(self, key, secret, account) -> None:
        self.key = key
        self.secret = secret
        self.account = account
        self.redis_client = redis.Redis(host="localhost", port=6379, db=0)

    def get_symbols(self) -> List:
        self.kis_client = mojito.KoreaInvestment(self.key, self.secret, self.account)
        markets = self.kis_client.fetch_symbols()
        symbols = [
            row["단축코드"]
            for _, row in markets.iterrows()
            if re.match(r"^\d", row["단축코드"])
        ]
        return symbols

    async def watch_data_loop(self, symbols):
        try:
            broker_ws = mojito.KoreaInvestmentWS(
                self.key, self.secret, ["H0STCNT0"], symbols
            )
            broker_ws.start()
            while True:
                try:
                    data_ = broker_ws.get()
                    data = data_[1]
                    symbol = data["유가증권단축종목코드"]
                    await self.put_data_in_redis(
                        symbol, json.dumps(data, ensure_ascii=False)
                    )
                except Exception as e:
                    print(f"Inner exception: {e}")
                    break
        except Exception as e:
            print(f"Outer exception: {e}")

    async def main(self):
        # 1세션당 40건 제한으로 사용 불가
        symbols = self.get_symbols()
        await self.watch_data_loop(symbols)

    async def put_data_in_redis(self, symbol, data):
        key = symbol
        value = data
        self.redis_client.set(key, value)


if __name__ == "__main__":
    # load_dotenv()
    # key = os.getenv("KIS_KEY")
    # secret = os.getenv("KIS_SECRET")
    # account = os.getenv("KIS_ACCOUNT")
    # kis = KISData(key, secret, account)
    # run(kis.main())

    upbit = UpbitData()
    run(upbit.main())
