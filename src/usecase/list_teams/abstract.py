from abc import ABC, abstractmethod

from domain.team.models import TeamFilterDTO


class AbstractListTeamUseCase(ABC):
    @abstractmethod
    async def execute(
        self, 
        filter_dto: TeamFilterDTO,
        offset: int = 0, 
        limit: int | None = None
    ):
        raise NotImplementedError()
