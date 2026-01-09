from abc import ABC, abstractmethod

from domain.token.models import UserLoginDTO


class AbstractCreateTokenUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: UserLoginDTO):
        raise NotImplementedError()
