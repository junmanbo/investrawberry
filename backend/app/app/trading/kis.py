import mojito
from pprint import pprint


class KIS:
    def __init__(self, access, secret, acc):
        self.exchange = mojito.KoreaInvestment(access, secret, acc)

    def get_balance(self):
        balance = self.exchange.fetch_balance()
        return balance
    
    def get_total_balance(self) -> dict:
        balances = self.get_balance()
        total_krw = int(balances.get("output2")[0].get("nass_amt"))
        balances = balances.get("output1")

        buying_krw = 0
        total_balance = {}

        for balance in balances:
            price  = int(float(balance.get("prpr")))
            amount = int(float(balance.get("hldg_qty")))
            avg_price = int(float(balance.get("pchs_avg_pric")))

            total_balance[balance.get("prdt_name")] = {
                "price": price,
                "amount": amount,
                "avg_price": avg_price,
                "notional": amount * avg_price
            }
            buying_krw += price * amount

        krw = total_krw - buying_krw
        total_balance["KRW"] = {
            "amount": krw, 
            "price": 1, 
            "avg_price": 1, 
            "notional": krw
        }

        return total_balance
        



if __name__ == "__main__":
    kis = KIS(key, secret, acc_no)
    balance = kis.get_total_balance()
    pprint(balance)

