from app import trading

# 거래소 클래스를 필요한 대로 추가
EXCHANGE_CLASSES = {"UPBIT": trading.Upbit, "KIS": trading.KIS}
