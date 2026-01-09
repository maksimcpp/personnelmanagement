from domain.token.models import AccessTokenDTO
from infrastructure.repositories.postgresql.token.uow import PostgreSQLTokenUnitOfWork
from usecase.get_user.abstract import AbstractGetUserUseCase


class PostgreSQLGetUserUseCase(AbstractGetUserUseCase):
    def __init__(self, uow: PostgreSQLTokenUnitOfWork):
        self._uow = uow

    async def execute(self, dto: AccessTokenDTO):
        async with self._uow as uow_:
            user = await uow_.token_repository.get_user(dto)
        return user
