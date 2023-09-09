from datetime import timedelta, datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app import crud, schemas, models
from app.api import deps
from app.core import security
from app.core.config import settings

router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
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
    user_in = schemas.UserUpdate(refresh_token=refresh_token, password=None)
    user = crud.user.update(db=db, db_obj=user, obj_in=user_in)

    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
        }
    )

    # Set HttpOnly and Secure options for the refresh token cookie
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        max_age=int(refresh_token_expires.total_seconds()),
        expires=refresh_expire,
        path="/login/refresh-token",
    )

    return response


@router.post("/login/refresh-token", response_model=schemas.Token)
async def login_refresh_token(
    current_user: models.User = Depends(deps.check_refresh),
) -> Any:
    """
    Refresh access token using the provided refresh token
    """

    # Generate a new access token
    now = datetime.now(timezone.utc)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_expire = now + access_token_expires
    access_token = security.create_access_token(current_user.id, expire=access_expire)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
async def logout(
    revoked_token: bool = Depends(deps.revoke_token),
) -> dict[str, str]:
    """
    Logout - token blacklisting
    """
    if revoked_token is True:
        return {"message": "success logout"}
    else:
        return {"message": "failed logout"}
