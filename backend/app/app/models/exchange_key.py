from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class ExchangeKey(Base):
    id = Column(Integer, primary_key=True, index=True)
    exchange_id = Column(Integer, ForeignKey("exchange.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    access_key = Column(String, nullable=False)
    secret_key = Column(String, nullable=False)
    account = Column(String)
    is_valid = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    exchange = relationship("Exchange", backref="exchange_keys")
    user = relationship("User", backref="exchange_keys")

