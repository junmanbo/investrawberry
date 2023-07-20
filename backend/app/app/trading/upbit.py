import ccxt
from pprint import pprint

class Upbit:
    def __init__(self, access=None, secret=None):
        self.exchange = ccxt.upbit({
            'apiKey': access,
            'secret': secret
        })

    def get_balance(self):
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
            notional = amount * avg_price
            if currency == "KRW":
                avg_price = 1
            elif notional < 100:
                continue
            total_balance[currency] = {
                "amount": amount,
                "avg_price": avg_price,
                "notional": amount * avg_price
            }
            
        return total_balance

    def get_market(self):
        markets = self.exchange.fetch_markets()
        return markets

    def place_order(self, **kwargs):
        order = self.exchange.create_order(kwargs.symbol, kwargs.order_type, kwargs.side, kwargs.amount, kwargs.price)
        

if __name__ == "__main__":
    upbit = Upbit()
    pprint(upbit.get_balance())

