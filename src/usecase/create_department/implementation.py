from domain.department.models import DepartmentCreateDTO
from infrastructure.repositories.postgresql.department.uow import PostgreSQLDepartmentUnitOfWork
from usecase.create_department.abstract import AbstractCreateDepartmentUseCase


class PostgreSQLCreateDepartmentUseCase(AbstractCreateDepartmentUseCase):
    def __init__(self, uow: PostgreSQLDepartmentUnitOfWork):
        self._uow = uow

    async def execute(self, dto: DepartmentCreateDTO):
        async with self._uow as uow_:
            department = await uow_.repository.create(dto)
        return department
