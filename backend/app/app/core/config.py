from dotenv import find_dotenv, load_dotenv
import os
import secrets
from typing import Any, Dict, List, Optional

from pydantic import AnyHttpUrl, EmailStr, PostgresDsn, validator
from pydantic_settings import BaseSettings

load_dotenv(find_dotenv(usecwd=True))


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    ACCESS_SECRET_KEY: str = secrets.token_urlsafe(32)
    REFRESH_SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    SERVER_NAME: str | None = os.getenv("SERVER_NAME", "")
    SERVER_HOST: str | AnyHttpUrl = os.getenv("SERVER_HOST", "http://localhost:8000")
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] | List = [
        "http://localhost:3000",
        "http://localhost",
        "http://duckdns.org",
        "http://backend.duckdns.org",
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "MyApp")
    POSTGRES_SERVER: str | None = os.getenv("POSTGRES_SERVER")
    POSTGRES_USER: str | None = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD: str | None = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_DB: str | None = os.getenv("POSTGRES_DB")
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=values.get("POSTGRES_DB") or "",
        )

    FIRST_SUPERUSER: EmailStr | str = os.getenv("FIRST_SUPERUSER", "admin")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD", "")
    FIRST_NAME: str = os.getenv("FIRST_NAME", "")
    USERS_OPEN_REGISTRATION: bool = True

    class Config:
        case_sensitive = True


settings = Settings()
