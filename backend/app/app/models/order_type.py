from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from app.db.base_class import Base


class OrderType(Base):
    id = Column(Integer, primary_key=True, index=True)
    order_type_nm = Column(String(20), nullable=False, unique=True)
    order_type_knm = Column(String(20), unique=True)
    order_type_desc = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

