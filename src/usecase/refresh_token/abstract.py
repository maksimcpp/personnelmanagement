from abc import ABC, abstractmethod

from domain.token.models import RefreshTokenDTO


class AbstractRefreshTokenUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: RefreshTokenDTO):
        raise NotImplementedError()
