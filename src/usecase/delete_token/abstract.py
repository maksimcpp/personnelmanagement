from abc import ABC, abstractmethod

from domain.token.models import AccessTokenDTO


class AbstractDeleteTokenUseCase(ABC):
    @abstractmethod
    async def execute(self, access_token: AccessTokenDTO):
        raise NotImplementedError()
