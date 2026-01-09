from abc import ABC, abstractmethod


class AbstractListTeamUseCase(ABC):
    @abstractmethod
    async def execute(self, offset: int = 0, limit: int | None = None):
        raise NotImplementedError()
