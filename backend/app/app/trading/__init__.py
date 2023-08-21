from .kis import KIS
from .upbit import Upbit
from app import models

# 거래소 클래스를 필요한 대로 추가
EXCHANGE_CLASSES = {"UPBIT": Upbit, "KIS": KIS}


def get_client(exchange_nm: str, key: models.ExchangeKey | None):
    if not key:
        access_key = None
        secret_key = None
        account = None
    else:
        access_key = key.access_key
        secret_key = key.secret_key
        account = key.account

    if exchange_nm in EXCHANGE_CLASSES:
        client_class = EXCHANGE_CLASSES[exchange_nm]
        client = client_class(access_key, secret_key, account)
        return client
    else:
        return None
