from domain.employee.models import EmployeeFilterDTO
from infrastructure.repositories.postgresql.employee.uow import PostgreSQLEmployeeUnitOfWork
from usecase.list_employees.abstract import AbstractListEmployeesUseCase


class PostgreSQLListEmployeesUseCase(AbstractListEmployeesUseCase):
    def __init__(self, uow: PostgreSQLEmployeeUnitOfWork):
        self._uow = uow

    async def execute(self, filter_dto: EmployeeFilterDTO):
        async with self._uow as uow_:
            employees = await uow_.employee_repository.list_employees(filter_dto)
        return employees
