from domain.team.models import TeamCreateDTO
from infrastructure.repositories.postgresql.team.uow import PostgreSQLTeamUnitOfWork
from infrastructure.repositories.postgresql.user.uow import PostgreSQLUserUnitOfWork
from usecase.create_team.abstract import AbstractCreateTeamUseCase


class PostgreSQLCreateTeamUseCase(AbstractCreateTeamUseCase):
    def __init__(self, uow: PostgreSQLTeamUnitOfWork):
        self._uow = uow

    async def execute(self, dto: TeamCreateDTO):
        async with self._uow as uow_:
            team = await uow_.repository.create(dto)
        return team
