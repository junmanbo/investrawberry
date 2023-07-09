import ccxt
from pprint import pprint

class Upbit:
    def __init__(self, access, secret):
        self.exchange = ccxt.upbit({
            'apiKey': access,
            'secret': secret
        })

    def get_balance(self):
        balance = self.exchange.fetch_balance()
        return balance

    def get_total_balance(self):
        total_balance = self.get_balance().get("total")
        return total_balance
        

if __name__ == "__main__":
    access = "vC1gCHjhxBzSeQYb2NiCoWNemnA7OYFc7GieQmdX"
    secret = "k2hknvsxzPpV5ca5RLJkwKHpwIYMxJYHcETkODUr"
    upbit = Upbit(access, secret)
    total_balance = upbit.get_total_balance()
    pprint(total_balance)

