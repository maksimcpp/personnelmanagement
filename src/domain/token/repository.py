from abc import ABC, abstractmethod

from domain.token.models import AccessTokenDTO, RefreshTokenDTO, TokenDeleteDTO
from domain.user.models import UserDTO


class AbstractTokenRepository(ABC):
    @abstractmethod
    async def create(self, user_dto: UserDTO):
        raise NotImplementedError()
    
    @abstractmethod
    async def delete(self, access_token: AccessTokenDTO):
        raise NotImplementedError()

    @abstractmethod
    async def refresh(self, refresh_token_dto: RefreshTokenDTO):
        raise NotImplementedError()

    @abstractmethod
    async def get_user(self, access_token: str):
        raise NotImplementedError()
