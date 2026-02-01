from typing import Optional
from infrastructure.repositories.postgresql.department.uow import PostgreSQLDepartmentUnitOfWork
from usecase.list_departments.abstract import AbstractListDepartmentUseCase


class PostgreSQLListDepartmentUseCase(AbstractListDepartmentUseCase):
    def __init__(self, uow: PostgreSQLDepartmentUnitOfWork):
        self._uow = uow

    async def execute(self, offset: int = 0, limit: Optional[int] = None):
        async with self._uow as uow_:
            departments = await uow_.repository.list_departments(
                limit=limit, offset=offset
            )
        return departments
