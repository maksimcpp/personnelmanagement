import datetime
import secrets

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.token.models import AccessTokenDTO, RefreshTokenDTO, TokenDTO, TokenDeleteDTO
from domain.token.repository import AbstractTokenRepository
from domain.user.models import UserDTO
from infrastructure.databases.postgresql.models import Token
from infrastructure.databases.postgresql.models.user import User
from infrastructure.repositories.postgresql.token.exceptions import TokenLifetimeExpired, TokenNotExist
from infrastructure.repositories.postgresql.user.exceptions import UserNotExist
from .hash import hash 


class PostgreSQLTokenRepository(AbstractTokenRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user_dto: UserDTO):
        access_token = secrets.token_urlsafe(56)
        refresh_token = secrets.token_urlsafe(56)

        hex_access_token = hash(access_token)
        hex_refresh_token = hash(refresh_token)

        refresh_token_expires_in = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)
        access_token_expires_in = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)

        token = Token(
            access_token=hex_access_token,
            refresh_token=hex_refresh_token,
            access_token_expires_in=access_token_expires_in,
            refresh_token_expires_in=refresh_token_expires_in,
            created_at=datetime.datetime.now(datetime.UTC),
            user_id=user_dto.id
        )

        self._session.add(token)
        await self._session.flush()

        return TokenDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_in=access_token_expires_in,
            refresh_token_expires_in=refresh_token_expires_in,
        )
    
    async def delete(self, access_token: AccessTokenDTO):
        query = select(Token).where(
            Token.access_token == hash(access_token.access_token)
        )
        result = await self._session.execute(query)
        token = result.scalar_one_or_none()

        if token is None:
            raise TokenNotExist()
        
        await self._session.delete(token)
        await self._session.flush()

    async def refresh(self, refresh_token_dto: RefreshTokenDTO):
        query = select(Token).where(
            Token.refresh_token == hash(refresh_token_dto.refresh_token)
        )
        result = await self._session.execute(query)
        token = result.scalar_one_or_none()

        if token is None:
            raise TokenNotExist()

        if datetime.datetime.now(datetime.UTC) > token.refresh_token_expires_in:
            raise TokenLifetimeExpired()
        
        access_token = secrets.token_urlsafe(56)
        refresh_token = secrets.token_urlsafe(56)

        hex_access_token = hash(access_token)
        hex_refresh_token = hash(refresh_token)

        refresh_token_expires_in = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=15)
        access_token_expires_in = datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=24)

        new_token = Token(
            access_token=hex_access_token,
            refresh_token=hex_refresh_token,
            access_token_expires_in=access_token_expires_in,
            refresh_token_expires_in=refresh_token_expires_in,
            created_at=datetime.datetime.now(datetime.UTC),
            user_id=token.user_id
        )

        await self._session.delete(token)
        self._session.add(new_token)
        await self._session.flush()

        return TokenDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            access_token_expires_in=access_token_expires_in,
            refresh_token_expires_in=refresh_token_expires_in,
        )
    
    async def get_user(self, token_dto: AccessTokenDTO):
        query = select(Token).where(
            Token.access_token == hash(token_dto.access_token)
        )
        result = await self._session.execute(query)
        token = result.scalar_one_or_none()

        if token is None:
            raise TokenNotExist()

        if datetime.datetime.now(datetime.UTC) > token.access_token_expires_in:
            raise TokenLifetimeExpired()
        
        query_user = select(User).join(Token, User.id == Token.user_id).where(
            Token.access_token == token.access_token
        )
        result_user = await self._session.execute(query_user)
        user = result_user.scalar_one_or_none()

        if user is None:
            raise UserNotExist()
        
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            last_name=user.last_name,
            first_name=user.first_name,
            patronymic=user.patronymic,
            is_admin=user.is_admin,
        )
