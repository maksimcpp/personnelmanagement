from infrastructure.repositories.postgresql.employee.uow import PostgreSQLEmployeeUnitOfWork
from usecase.set_team_to_employee.abstract import AbstractSetTeamIdUseCase


class PostgreSQLSetTeamIdUseCase(AbstractSetTeamIdUseCase):
    def __init__(self, uow: PostgreSQLEmployeeUnitOfWork):
        self._uow = uow

    async def execute(self, team_id: int, employee_id: int):
        async with self._uow as uow_:
            employee = await uow_.employee_repository.set_team(
                team_id=team_id,
                employee_id=employee_id
            )
        return employee
