from datetime import datetime, timedelta

from app import models, crud, schemas
from app.api import deps

db = next(deps.get_db())


portfolio_list = crud.portfolio.get_portfolio_running(db=db, is_running=True)


for portfolio in portfolio_list:
    now = datetime.now().date()
    if portfolio.rebal_dt is None:
        rebal_dt = portfolio.created_at + timedelta(days=portfolio.rebal_period)
        rebal_dt = rebal_dt.date()
    else:
        rebal_dt = portfolio.rebal_dt + timedelta(days=portfolio.rebal_period)

    if now > rebal_dt:
        # 주문 실행 celery
        print(f"id: {portfolio.id} now: {now} > rebalancing: {rebal_dt} 이므로 주문을 실행합니다.")

        portfolio_in = schemas.PortfolioUpdate(rebal_dt=now.strftime("%Y-%m-%d"))
        crud.portfolio.update(db=db, db_obj=portfolio, obj_in=portfolio_in)
