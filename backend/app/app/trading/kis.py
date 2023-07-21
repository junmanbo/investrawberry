import mojito
from pprint import pprint


class KIS:
    def __init__(self, access: str, secret: str, acc: str):
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

    def get_market(self):
        markets = self.exchange.fetch_symbols()
        return markets
        
    def place_order(self, params):
        side = params.side.lower()

        # 주문 유형 번호 설정
        order_type = params.order_type.lower()
        if order_type == "limit":
            order_type = "00"
        elif order_type == "market":
            order_type = "01"

        order = self.exchange.create_order(side, params.symbol, params.price, params.quantity, order_type)
        order["id"] = order["output"]["ODNO"]

        return order

    def check_order(self, uuid):
        params = {
            "CTX_AREA_FK100": "",
            "CTX_AREA_NK100": "",
            "INQR_DVSN_1": "1",
            "INQR_DVSN_2": "0"
        }
        orders = self.exchange.fetch_open_order(params)
        for order in orders:
            if order["output"]["odno"] == uuid:

        return order

    def cancel_order(self, uuid):
        order = self.exchange.cancel_order("", uuid, 0, True)
        return order



if __name__ == "__main__":
    kis = KIS(key, secret, acc_no)
    markets = kis.get_market()
    print(markets.head(5))

