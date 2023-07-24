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

        quantity = int(params.quantity)
        price = int(params.price)
        order = self.exchange.create_order(side=side, 
                                           symbol=params.ticker.symbol, 
                                           price=price, 
                                           quantity=quantity,
                                           order_type=order_type)
        try:
            order["id"] = order["output"]["ODNO"]
        except KeyError:
            return order
        return order

    def check_order(self, uuid):
        orders = self.exchange.fetch_order(uuid)

        ord_qty = int(orders["output2"]["tot_ord_qty"])
        filled_qty = int(orders["output2"]["tot_ccld_qty"])

        # 상태 업데이트
        if ord_qty == filled_qty:
            if ord_qty == 0:
                orders["status"] = "canceled"
            else:
                orders["status"] = "closed"
        else:
            orders["status"] = "open"

        orders["filled"] = int(orders["output2"]["tot_ccld_qty"]) # 체결 수량
        orders["average"] = int(float(orders["output2"]["pchs_avg_pric"])) # 체결 금액
        orders["fee"] = {"cost": int(orders["output2"]["prsm_tlex_smtl"])} # 수수료+세금

        return orders

    def cancel_order(self, uuid):
        order = self.exchange.cancel_order("", uuid, 0, True)
        return order


if __name__ == "__main__":
    kis = KIS(key, secret, acc_no)
    markets = kis.get_market()
    print(markets.head(5))

