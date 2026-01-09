from abc import ABC, abstractmethod

from domain.token.models import AccessTokenDTO


class AbstractGetUserUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: AccessTokenDTO):
        raise NotImplementedError()
