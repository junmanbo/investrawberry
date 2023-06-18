from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Time

from app.db.base_class import Base


class Exchange(Base):
    id = Column(Integer, primary_key=True, index=True)
    exchange_nm = Column(String, index=True)
    open_time = Column(Time, nullable=False)
    close_time = Column(Time,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

