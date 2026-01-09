from abc import ABC, abstractmethod

from domain.user.models import UserCreateDTO


class AbstractCreateUserUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: UserCreateDTO):
        raise NotImplementedError()
