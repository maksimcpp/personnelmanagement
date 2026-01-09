from abc import ABC, abstractmethod

from domain.token.models import UserLoginDTO
from domain.user.models import UserCreateDTO


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create(self, dto: UserCreateDTO):
        raise NotImplementedError()
    
    async def get(self, dto: UserLoginDTO):
        raise NotImplementedError()
