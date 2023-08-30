from typing import Generator
from datetime import datetime, timezone
import json
import redis
import os

from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, exceptions
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)

REDIS_HOSTNAME = os.getenv("REDIS_HOSTNAME", "localhost")


def get_db() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.ACCESS_SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has expired",
        )
    except (exceptions.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    # check user
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # check blacklist
    r = redis.Redis(host=REDIS_HOSTNAME, port=6379, db=1)
    black_token = r.get(user.id)
    if black_token:
        black_token = json.loads(black_token)
    if black_token == token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token in blacklist",
        )
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user


def revoke_token(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> bool:
    try:
        payload = jwt.decode(
            token, settings.ACCESS_SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has expired",
        )
    except (exceptions.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    now = datetime.now(timezone.utc)
    exp_datetime = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    remaining_time = int((exp_datetime - now).total_seconds())

    r = redis.Redis(host=REDIS_HOSTNAME, port=6379, db=1)
    r.set(user.id, json.dumps(token))
    r.expire(user.id, remaining_time)

    user_in = schemas.UserUpdate(refresh_token=None, password=None)
    crud.user.update(db=db, db_obj=user, obj_in=user_in)
    return True


def check_refresh(
    db: Session = Depends(get_db), token: str = Cookie(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.REFRESH_SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token has expired",
        )
    except (exceptions.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    # check user
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if token != user.refresh_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    return user
