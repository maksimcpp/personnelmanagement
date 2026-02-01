from domain.team.models import TeamFilterDTO
from infrastructure.repositories.postgresql.team.uow import PostgreSQLTeamUnitOfWork
from usecase.list_teams.abstract import AbstractListTeamUseCase


class PostgreSQLListTeamUseCase(AbstractListTeamUseCase):
    def __init__(self, uow: PostgreSQLTeamUnitOfWork):
        self._uow = uow

    async def execute(
        self, 
        filter_dto: TeamFilterDTO,
    ):
        async with self._uow as uow_:
            teams = await uow_.repository.list_teams(
                filter_dto=filter_dto,
            )
        return teams
