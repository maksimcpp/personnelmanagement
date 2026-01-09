from domain.token.models import AccessTokenDTO, UserLoginDTO
from infrastructure.repositories.postgresql.token.uow import PostgreSQLTokenUnitOfWork
from usecase.delete_token.abstract import AbstractDeleteTokenUseCase


class PostgreSQLDeleteTokenUseCase(AbstractDeleteTokenUseCase):
    def __init__(self, uow: PostgreSQLTokenUnitOfWork):
        self._uow = uow

    async def execute(self, access_token: AccessTokenDTO):
        async with self._uow as uow_:
            token = await uow_.token_repository.delete(access_token)
        return token
