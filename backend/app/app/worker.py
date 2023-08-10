from typing import Any
import time
from pprint import pprint

from app.core.celery_app import celery_app
from app import crud, schemas, models
from app.api import deps
from app.trading import upbit, kis


@celery_app.task(acks_late=True)
def place_order(transaction_id: int) -> Any:
    db = next((deps.get_db()))
    transaction = crud.transaction.get(db=db, id=transaction_id)
    if transaction is None:
        return {"message": "Transaction is not found."}
    exchange = transaction.ticker.exchange

    # 키 정보 가져오기
    key = crud.exchange_key.get_key_by_owner_exchange(
        db, owner_id=transaction.user_id, exchange_id=exchange.id
    )

    if exchange.exchange_nm == "UPBIT":
        client = upbit.Upbit(key.access_key, key.secret_key)
    elif exchange.exchange_nm == "KIS":
        client = kis.KIS(key.access_key, key.secret_key, key.account)
    else:
        return {"message": "Exchange is not found."}

    order = client.place_order(transaction)
    # if order["rt_cd"] != "0":
    #     return order["msg1"]

    transaction_in = schemas.TransactionUpdate(uuid=order["id"], status="open")
    crud.transaction.update(db=db, db_obj=transaction, obj_in=transaction_in)

    while True:
        order_result = client.check_order(transaction_in.uuid)
        print(order_result)

        transaction_in.quantity = order_result["filled"]
        transaction_in.fee = order_result["fee"]["cost"]
        transaction_in.status = order_result["status"]

        # 취소한 경우 average 가 none 값.
        if order_result["average"] is None:
            transaction_in.price = transaction.price
        else:
            transaction_in.price = order_result["average"]

        # open 이 아니면 업데이트하고 종료
        if order_result["status"] != "open":
            crud.transaction.update(db=db, db_obj=transaction, obj_in=transaction_in)
            return order_result

        time.sleep(0.5)


@celery_app.task(acks_late=True)
def portfolio_order(pf: models.Portfolio) -> Any:
    db = next((deps.get_db()))

    # 계좌 잔고 전체 가져오기
    exchange_keys = crud.exchange_key.get_multi_by_owner(db, owner_id=pf.user_id)
    total_balance = {}
    for key in exchange_keys:
        if key.exchange.exchange_nm == "UPBIT":
            client = upbit.Upbit(key.access_key, key.secret_key)
        elif key.exchange.exchange_nm == "KIS":
            client = kis.KIS(key.access_key, key.secret_key, key.account)
        else:
            return {"message": "Exchange is not found."}
        balance = client.get_total_balance()
        total_balance[key.exchange.exchange_nm] = balance

    pf_tickers = crud.portfolio_ticker.get_by_portfolio_id(db=db, portfolio_id=pf.id)
    if pf_tickers is None:
        return {"message": "Portfolio Tickers are not found."}

    # 포트폴리오에 있는 티커의 총 금액 구하기
    total_amount = 0
    for pf_ticker in pf_tickers:
        exchange = pf_ticker.ticker.exchange
        ticker = pf_ticker.ticker
        try:
            current_amount = total_balance[exchange.exchange_nm][ticker.symbol][
                "notional"
            ]
        except TypeError as e:
            print(e)
            current_amount = 0

        total_amount += current_amount

    # total_amount = 0 or current_amount = 0 인 경우 (처음)

    # 총 금액으로 각 티커의 비중을 계산하고 필요한 만큼 매매
    for pf_ticker in pf_tickers:
        exchange = pf_ticker.ticker.exchange
        ticker = pf_ticker.ticker
        try:
            # 현재 보유 자산의 평가 금액
            current_amount = total_balance[exchange.exchange_nm][ticker.symbol][
                "notional"
            ]
        except TypeError as e:
            print(e)
            current_amount = 0

        if current_amount == 0:
            ticker_amount = int(pf.amount * pf_ticker.weight / 100)
            ticker_quantity = ticker_amount / current_price
            transaction_in = schemas.TransactionCreate(
                user_id=pf.user_id,
                ticker_id=ticker.id,
                side="buy",
                price=current_price,
                quantity=ticker_quantity,
                order_type="market",
            )
            crud.transaction.create(db=db, obj_in=transaction_in)
        else:
            current_weight = current_amount / total_amount * 100
            if current_weight > pf_ticker.weight:
                trade_amount = (
                    current_amount * (current_weight - pf_ticker.weight) / 100
                )
                trade_quantity = trade_amount / current_price

        print(ticker_amount)

    return {"message": "success"}
