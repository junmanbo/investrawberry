from typing import Any
import ccxt
from pprint import pprint
import redis
import json


class Upbit:
    def __init__(self, access: str | None, secret: str | None, _: str | None):
        self.exchange = ccxt.upbit({"apiKey": access, "secret": secret})
        self.r = redis.Redis(host="localhost", port=6379, db=0)

    def get_balance(self) -> Any:
        balance = self.exchange.fetch_balance()
        return balance

    def get_total_balance(self):
        total_balance = {}
        balances = self.get_balance()
        balances = balances.get("info")
        for balance in balances:
            currency = balance.get("currency")
            avg_price = int(float(balance.get("avg_buy_price")))
            amount = float(balance.get("balance"))
            price = self.get_price(symbol=currency)
            if currency == "KRW":
                avg_price = 1
                price = 1

            notional = amount * price
            # 자산 평가금액이 10원 미만이면 리스트에서 제외
            if notional < 10:
                continue
            avg_notional = avg_price * amount

            return_rate = (price - avg_price) / avg_price * 100
            return_profit = notional - avg_notional
            total_balance[currency] = {
                "amount": amount,
                "avg_price": avg_price,
                "notional": notional,
                "price": price,
                "return_rate": return_rate,
                "return_profit": return_profit,
            }

        return total_balance

    def get_market(self):
        markets = self.exchange.fetch_markets()
        return markets

    def place_order(self, params):
        symbol = f"{params.ticker.symbol}/{params.ticker.currency}"  # ccxt 에 맞는 symbol
        side = params.side.lower()
        order_type = params.order_type.lower()

        # 수수료 뺀 만큼 주문 Insufficient Balance 방지
        fee_rate = 0
        if order_type == "market":
            fee_rate = params.ticker.taker_fee
        if order_type == "limit":
            fee_rate = params.ticker.maker_fee
        quantity = params.quantity * (1 - fee_rate)

        order = self.exchange.create_order(
            symbol, order_type, side, quantity, params.price
        )
        return order

    def check_order(self, uuid):
        order = self.exchange.fetch_order(id=uuid)
        return order

    def cancel_order(self, uuid):
        order = self.exchange.cancel_order(id=uuid)
        return order

    def get_price(self, symbol, currency="KRW"):
        price_data = self.r.get(f"{symbol}/{currency}")
        if price_data:
            price_data = json.loads(price_data)
            price = price_data.get("close")
        elif symbol == "KRW":
            price = 1
        else:
            price = 0
        return price


if __name__ == "__main__":
    upbit = Upbit(None, None, None)
    pprint(upbit.get_balance())
