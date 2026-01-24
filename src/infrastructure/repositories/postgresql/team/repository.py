from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domain.team.models import TeamCreateDTO, TeamDTO, TeamFilterDTO
from domain.team.repository import AbstractTeamRepository
from infrastructure.databases.postgresql.models.team import Team
from infrastructure.repositories.postgresql.team.exceptions import InvalidDepartmentId


class PostgreSQLTeamRepository(AbstractTeamRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, dto: TeamCreateDTO):
        team = Team(
            name=dto.name,
            department_id=dto.department_id
        )
        self._session.add(team)

        try:
            await self._session.flush()
        except IntegrityError:
            raise InvalidDepartmentId()

        return TeamDTO(
            id=team.id,
            name=team.name,
            department_id=team.department_id
        )
    
    async def list(self, filter_dto: TeamFilterDTO):
        query = select(Team)
        filters = []
        if filter_dto.department_id is not None:
            filters.append(Team.department_id == filter_dto.department_id)

        if filters:
            query = query.filter(and_(*filters))

        result = await self._session.execute(query)
        teams = result.scalars().all()
        teams_dto = [
            TeamDTO(
                id=team.id,
                name=team.name,
                department_id=team.department_id
            ) for team in teams
        ]
        return teams_dto
