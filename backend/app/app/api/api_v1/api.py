from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    login,
    users,
    exchanges,
    exchangekeys,
    balance,
    ticker,
    order,
    portfolio,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(exchanges.router, prefix="/exchanges", tags=["exchanges"])
api_router.include_router(
    exchangekeys.router, prefix="/exchangekeys", tags=["exchangekeys"]
)
api_router.include_router(balance.router, prefix="/balance", tags=["balance"])
api_router.include_router(ticker.router, prefix="/ticker", tags=["ticker"])
api_router.include_router(order.router, prefix="/order", tags=["order"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
