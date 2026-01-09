from infrastructure.repositories.postgresql.employee.uow import PostgreSQLEmployeeUnitOfWork
from usecase.list_employees.abstract import AbstractListEmployeesUseCase
from usecase.list_employees_by_status.abstract import AbstractListEmployeesByStatusUseCase
from utils.enums import EmployeeStatus


class PostgreSQLListEmployeesByStatusUseCase(AbstractListEmployeesByStatusUseCase):
    def __init__(self, uow: PostgreSQLEmployeeUnitOfWork):
        self._uow = uow

    async def execute(self, employee_status: EmployeeStatus):
        async with self._uow as uow_:
            employees = await uow_.employee_repository.list_by_status(employee_status)
        return employees
