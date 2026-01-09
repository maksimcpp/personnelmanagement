from datetime import datetime
from pydantic import BaseModel


class TokenSchema(BaseModel):
    refresh_token: str
    access_token: str
    refresh_token_expires_in: datetime
    access_token_expires_in: datetime


class UserLoginSchema(BaseModel):
    username: str
    password: str


class RefreshTokenSchema(BaseModel):
    refresh_token: str


class AccessTokenSchema(BaseModel):
    access_token: str
