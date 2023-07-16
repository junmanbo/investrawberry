from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text

from app.db.base_class import Base


class Strategy(Base):
    """매매 전략"""

    id = Column(Integer, primary_key=True, index=True)
    strategy_nm = Column(String(20), nullable=False, unique=True)
    strategy_knm = Column(String(20), nullable=False, unique=True)
    strategy_desc = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

