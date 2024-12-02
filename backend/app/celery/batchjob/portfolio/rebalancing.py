import logging
from datetime import datetime, timedelta

from app import crud, schemas
from app import trading
from app.api import deps

# import a celery module
from celery import Celery
from celery.schedules import crontab
from celery.schedules import timedelta as ct

# 로깅 설정
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# celery settings
app = Celery("rebalancing", broker="redis://localhost:6379/1")

app.conf.update(
    broker_connection_retry_on_startup=True,
    beat_schedule={
        "check_rebalancing-every-afternoon": {
            "task": "rebalancing.check_rebalancing",
            "schedule": ct(seconds=30),
            # "schedule": crontab(hour=16, minute=5),
            "options": {"timezone": "Asia/Seoul"},
        },
    },
)


@app.task
def check_rebalancing():
    db = next(deps.get_db())

    portfolio_list = crud.portfolio.get_portfolio_running(db=db, is_running=True)

    for portfolio in portfolio_list:
        now = datetime.now().date()
        if portfolio.rebal_dt is None:
            rebal_dt = portfolio.created_at + timedelta(days=portfolio.rebal_period)
            rebal_dt = rebal_dt.date()
        else:
            rebal_dt = portfolio.rebal_dt + timedelta(days=portfolio.rebal_period)

        print(f"Rebalancing task started!\nrebalancing date: {rebal_dt}")

        # 현재시간이 리밸런싱 해야 되는 시간보다 클 경우 리밸런싱 매매 진행
        if now > rebal_dt:
            print(
                f"id: {portfolio.id} now: {now} > rebalancing: {rebal_dt} 이므로 주문을 실행합니다."
            )
            exchange_keys = crud.exchange_key.get_multi_by_owner(
                db, owner_id=portfolio.user_id
            )
            total_balance = {}
            for key in exchange_keys:
                exchange_nm = key.exchange.exchange_nm
                client = trading.get_client(exchange_nm, key)
                balance = client.get_total_balance()
                total_balance[exchange_nm] = balance

            # print(total_balance)

            portfolio_tickers = crud.portfolio_ticker.get_by_portfolio_id(
                db=db, portfolio_id=portfolio.id
            )
            for ticker in portfolio_tickers:
                print(ticker.ticker_id)

            # portfolio_in = schemas.PortfolioUpdate(rebal_dt=now.strftime("%Y-%m-%d"))
            # crud.portfolio.update(db=db, db_obj=portfolio, obj_in=portfolio_in)
        else:
            print(f"id: {portfolio.id} now: {now} < rebalancing: {rebal_dt} 주문X")
