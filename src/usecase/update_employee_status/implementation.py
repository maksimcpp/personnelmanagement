from infrastructure.repositories.postgresql.employee.uow import PostgreSQLEmployeeUnitOfWork
from usecase.update_employee_status.abstract import AbstractUpdateEmployeeStatusUseCase
from utils.enums import EmployeeStatus


class PostgreSQLUpdateEmployeeStatusUseCase(AbstractUpdateEmployeeStatusUseCase):
    def __init__(self, uow: PostgreSQLEmployeeUnitOfWork):
        self._uow = uow

    async def execute(self, employee_id: int, status: EmployeeStatus):
        async with self._uow as uow_:
            employee = await uow_.employee_repository.update_status(
                employee_id=employee_id,
                status=status
            )
        return employee
