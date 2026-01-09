from abc import ABC, abstractmethod

from domain.user.models import UserDTO


class AbstractGetCurrentEmployeeUseCase(ABC):
    @abstractmethod
    async def execute(
        self,
        user_dto: UserDTO    
    ):
        raise NotImplementedError()
