from infrastructure.repositories.postgresql.team.uow import PostgreSQLTeamUnitOfWork
from usecase.list_teams.abstract import AbstractListTeamUseCase


class PostgreSQLListTeamUseCase(AbstractListTeamUseCase):
    def __init__(self, uow: PostgreSQLTeamUnitOfWork):
        self._uow = uow

    async def execute(self, offset: int = 0, limit: int | None = None):
        async with self._uow as uow_:
            teams = await uow_.repository.list()
        
        if limit is not None:
            return teams[offset: offset + limit]
        else:
            return teams[offset:]
