# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base
from app.models.asset_type import AssetType
from app.models.exchange import Exchange
from app.models.exchange_key import ExchangeKey
from app.models.portfolio import (
    Portfolio,
    PortfolioTicker,
)
from app.models.ticker import Ticker
from app.models.user import User
