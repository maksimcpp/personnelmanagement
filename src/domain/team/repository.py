from abc import ABC, abstractmethod

from domain.team.models import TeamCreateDTO, TeamRenameDTO


class AbstractTeamRepository(ABC):
    @abstractmethod
    async def create(self, dto: TeamCreateDTO):
        raise NotImplementedError()
    
    @abstractmethod
    async def list(self):
        raise NotImplementedError()
