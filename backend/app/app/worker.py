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
    if not transaction:
        raise Exception("Transaction not found")
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
        raise Exception("Exchange not found")

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
def portfolio_order(pf_id: int) -> Any:
    db = next((deps.get_db()))

    # portfolio id 로 portfolio 조회
    pf = crud.portfolio.get(db=db, id=pf_id)
    if not pf:
        raise Exception("Portfoilio not found")

    # 계좌 잔고 전체 가져오기
    exchange_keys = crud.exchange_key.get_multi_by_owner(db, owner_id=pf.user_id)
    total_balance = {}
    for key in exchange_keys:
        if key.exchange.exchange_nm == "UPBIT":
            client = upbit.Upbit(key.access_key, key.secret_key)
        elif key.exchange.exchange_nm == "KIS":
            client = kis.KIS(key.access_key, key.secret_key, key.account)
        else:
            raise Exception("Exchange not found")
        balance = client.get_total_balance()
        total_balance[key.exchange.exchange_nm] = balance

    pf_tickers = crud.portfolio_ticker.get_by_portfolio_id(db=db, portfolio_id=pf.id)
    if not pf_tickers:
        raise Exception("Portfolio Tickers not found")

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

        current_price = total_balance[exchange.exchange_nm][ticker.symbol][
            "price"
        ]  # 현재가
        current_weight = current_amount / pf.amount * 100  # 현재 비중

        diff_weight = current_weight - pf_ticker.weight  # 현재 비중과 포트폴리오 비중 차이 (%단위)
        diff_amount = abs(diff_weight) * pf.amount / 100  # 비중 차이에 대한 주문 금액
        diff_quantity = diff_amount / current_price  # 주문 금액을 현재가로 나누면 주문 수량

        # 비중이 지정한 비중보다 많으면 매도
        # 비중이 지정한 비중보다 적으면 매수
        if diff_weight > 0:
            side = "sell"
        else:
            side = "buy"

        transaction_in = schemas.TransactionCreate(
            user_id=pf.user_id,
            ticker_id=ticker.id,
            side=side,
            price=current_price,
            quantity=diff_quantity,
            order_type="market",
        )
        transaction = crud.transaction.create(db=db, obj_in=transaction_in)
        print(transaction)

    return {"message": "success"}
