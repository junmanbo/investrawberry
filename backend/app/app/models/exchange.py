from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Time, Boolean

from app.db.base_class import Base


class Exchange(Base):
    id = Column(Integer, primary_key=True, index=True)
    exchange_nm = Column(String(50), index=True)
    exchange_knm = Column(String(50))
    open_time = Column(Time, nullable=False)
    close_time = Column(Time,nullable=False)
    is_summer = Column(Boolean(), default=False)
    min_interval = Column(Integer, default=0.3)
    min_amount = Column(Integer)
    min_digit = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

