from sqlalchemy.ext.asyncio import AsyncSession

from domain.department.repository import AbstractDepartmentRepository
from infrastructure.repositories.postgresql.department.repository import PostgreSQLDepartmentRepository


class PostgreSQLDepartmentUnitOfWork:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session
        self.repository: AbstractDepartmentRepository | None = None

    async def __aenter__(self):
        self.repository = PostgreSQLDepartmentRepository(self._session)
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
