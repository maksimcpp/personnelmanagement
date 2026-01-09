from abc import ABC, abstractmethod

from domain.team.models import TeamCreateDTO


class AbstractCreateTeamUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: TeamCreateDTO):
        raise NotImplementedError()
