from datetime import datetime
from sqlalchemy import Boolean, Column, Integer, String, DateTime, Index

from app.db.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(50))
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)
    is_vip = Column(Boolean(), default=False)
    refresh_token = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
