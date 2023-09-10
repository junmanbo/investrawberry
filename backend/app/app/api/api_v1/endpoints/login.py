from datetime import timedelta, datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings

router = APIRouter()


@router.post("/login/access-token")
async def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")

    # access token 생성
    now = datetime.now(timezone.utc)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_expire = now + access_token_expires
    access_token = security.create_access_token(user.id, expire=access_expire)

    # refresh token 생성
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_expire = now + refresh_token_expires
    refresh_token = security.create_refresh_token(user.id, expire=refresh_expire)

    content = {
        "access_token": access_token,
        "token_type": "Bearer",
        "user_name": user.full_name,
    }
    response = JSONResponse(content=content)

    # Set HttpOnly and Secure options for the refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,
        max_age=int(refresh_token_expires.total_seconds()),
        expires=refresh_expire,
        path="/",
    )

    return response


@router.post("/login/refresh-token")
async def login_refresh_token(refresh_token: str = Cookie(default=None)) -> Any:
    """
    Refresh access token using the provided refresh token
    """
    user = deps.check_refresh(token=refresh_token)
    # Generate a new access token
    now = datetime.now(timezone.utc)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_expire = now + access_token_expires
    access_token = security.create_access_token(user.id, expire=access_expire)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "user_name": user.full_name,
    }


@router.post("/logout")
async def logout() -> Any:
    """
    Logout - token blacklisting
    """
    content = {"message": "success logout"}
    response = JSONResponse(content=content)
    response.delete_cookie(key="refresh_token", path="/")
    return response
