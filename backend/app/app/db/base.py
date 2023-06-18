# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base
from app.models.user import User
from app.models.exchange import Exchange
from app.models.exchange_key import ExchangeKey
