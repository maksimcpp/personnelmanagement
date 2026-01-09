from sqlalchemy.ext.asyncio import AsyncSession

from domain.token.repository import AbstractTokenRepository
from domain.user.repository import AbstractUserRepository
from infrastructure.repositories.postgresql.token.repository import PostgreSQLTokenRepository
from infrastructure.repositories.postgresql.user.repository import PostgreSQLUserRepository


class PostgreSQLTokenUnitOfWork:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session
        self.user_repository: AbstractUserRepository | None = None
        self.token_repository: AbstractTokenRepository | None = None

    async def __aenter__(self):
        self.user_repository = PostgreSQLUserRepository(self._session)
        self.token_repository = PostgreSQLTokenRepository(self._session)
        return self

    async def __aexit__(self, exc_type: Exception | None, exc_value, traceback):
        if exc_type is not None:
            await self._session.rollback()
        await self.commit()
        await self._session.close()
        self.repository = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
