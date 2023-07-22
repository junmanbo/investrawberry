import time
from pprint import pprint

from app.core.celery_app import celery_app
from app import crud, schemas
from app.api import deps
from app.trading import upbit, kis


@celery_app.task(acks_late=True)
def place_order(simple_transaction_id) -> str:
    db = next((deps.get_db()))
    st = crud.simple_transaction.get(db, simple_transaction_id)
    exchange = st.ticker.exchange

    # 키 정보 가져오기
    key = crud.exchange_key.get_key_by_owner_exchange(db, owner_id=st.user_id, exchange_id=exchange.id)

    if exchange.exchange_nm == "UPBIT":
        client = upbit.Upbit(key.access_key, key.secret_key)
    elif exchange.exchange_nm == "KIS":
        client = kis.KIS(key.access_key, key.secret_key, key.account)

    order = client.place_order(st)

    st_in = schemas.SimpleTransactionUpdate(uuid=order["id"], status="open")
    crud.simple_transaction.update(db=db, db_obj=st, obj_in=st_in)

    while True:
        order_result = client.check_order(st_in.uuid)
        order_result = order_result

        st_in.quantity = order_result["filled"]
        st_in.fee = order_result["fee"]["cost"]
        st_in.status = order_result["status"]
        st_in.price = order_result["average"]

        if order_result["status"] == "done" or order_result["status"] == "closed":
            crud.simple_transaction.update(db=db, db_obj=st, obj_in=st_in)
            return order_result
        elif order_result["status"] == "canceled":
            crud.simple_transaction.update(db=db, db_obj=st, obj_in=st_in)
            return order_result

        time.sleep(0.5)
