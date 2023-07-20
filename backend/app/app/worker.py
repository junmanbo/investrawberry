import ccxt
import mojito

from app.core.celery_app import celery_app
from app import crud
from app.api import deps
from app.trading import upbit, kis


@celery_app.task(acks_late=True)
def place_order(simple_transaction_id) -> str:
    db = next((deps.get_db()))
    st = crud.simple_transaction.get(db, simple_transaction_id)
    exchange = st.ticker.exchange

    key = crud.exchange_key.get_key_by_owner_exchange(db, owner_id=st.user_id, exchange_id=exchange.id)

    if exchange.exchange_nm == "UPBIT":
        client = upbit.Upbit(key.access_key, key.secret_key)
    elif exchange.exchange_nm == "KIS":
        client = kis.KIS(key.access_key, key.secret_key, key.account)

    order = client.place_order(st)

    return order
