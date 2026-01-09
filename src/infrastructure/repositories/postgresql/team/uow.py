from sqlalchemy.ext.asyncio import AsyncSession

from domain.team.repository import AbstractTeamRepository
from infrastructure.repositories.postgresql.team.repository import PostgreSQLTeamRepository


class PostgreSQLTeamUnitOfWork:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session
        self.repository: AbstractTeamRepository | None = None

    async def __aenter__(self):
        self.repository = PostgreSQLTeamRepository(self._session)
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
