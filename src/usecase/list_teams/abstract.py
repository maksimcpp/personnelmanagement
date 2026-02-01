from abc import ABC, abstractmethod

from domain.team.models import TeamFilterDTO


class AbstractListTeamUseCase(ABC):
    @abstractmethod
    async def execute(
        self, 
        filter_dto: TeamFilterDTO,
    ):
        raise NotImplementedError()
