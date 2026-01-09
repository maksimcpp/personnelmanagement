from sqlalchemy.ext.asyncio import AsyncSession

from domain.employee.repository import AbstractEmployeeRepository
from domain.user.repository import AbstractUserRepository
from infrastructure.repositories.postgresql.employee.repository import PostgreSQLEmployeeRepository
from infrastructure.repositories.postgresql.user.repository import PostgreSQLUserRepository


class PostgreSQLEmployeeUnitOfWork:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session
        self.user_repository: AbstractUserRepository | None = None
        self.employee_repository: AbstractEmployeeRepository | None = None

    async def __aenter__(self):
        self.user_repository = PostgreSQLUserRepository(self._session)
        self.employee_repository = PostgreSQLEmployeeRepository(self._session)
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
