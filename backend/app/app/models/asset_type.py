from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

from app.db.base_class import Base


class AssetType(Base):
    """자산 유형"""

    id = Column(Integer, primary_key=True, index=True)
    asset_nm = Column(String(20), nullable=False, unique=True)
    asset_knm = Column(String(20), nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

