from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str
    user_name: str | None = None


class TokenPayload(BaseModel):
    sub: int
    usage: str
