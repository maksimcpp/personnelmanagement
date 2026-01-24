from dataclasses import dataclass
from datetime import datetime


@dataclass
class TokenDTO:
    refresh_token: str
    access_token: str
    refresh_token_expires_in: datetime
    access_token_expires_in: datetime


@dataclass
class UserLoginDTO:
    username: str
    password: str


@dataclass
class RefreshTokenDTO:
    refresh_token: str


@dataclass
class AccessTokenDTO:
    access_token: str
