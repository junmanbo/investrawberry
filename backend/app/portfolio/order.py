from app import models
from app.api import deps
from app import crud

db = next(deps.get_db())

ticker = crud.ticker.get(db=db, id=1)
print(ticker.ticker_knm)
