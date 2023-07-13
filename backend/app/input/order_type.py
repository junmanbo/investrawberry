from app.db.session import SessionLocal
from app.crud.order_type import order_type
from app.schemas.order_type import OrderTypeCreate


# Create a new session
session = SessionLocal()

data_list = [
    {"order_type_nm": "SIMPLE", "order_type_knm": "시장가", "order_type_desc": "시장가로 내는 단순 주문"},
    {"order_type_nm": "TWAP", "order_type_knm": "시간 분할 주문", "order_type_desc": "시장가로 일정한 간격으로 분할해서 내는 주문"},
    {"order_type_nm": "VWAP", "order_type_knm": "거래량 분할 주문", "order_type_desc": "지정가로 거래량에 따라 분할해서 내는 주문"}
]

for data in data_list:
    print(data)
    order_type_data = OrderTypeCreate(
        order_type_nm=data['order_type_nm'],
        order_type_knm=data['order_type_knm'],
        order_type_desc=data['order_type_desc']
    )
    # Add the new Ticker object to the database using the CRUD object
    order_type.create(session, obj_in=order_type_data)

# Close the session
session.close()


