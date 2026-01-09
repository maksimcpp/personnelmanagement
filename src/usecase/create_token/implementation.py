from domain.token.models import UserLoginDTO
from infrastructure.repositories.postgresql.token.uow import PostgreSQLTokenUnitOfWork
from usecase.create_token.abstract import AbstractCreateTokenUseCase


class PostgreSQLCreateTokenUseCase(AbstractCreateTokenUseCase):
    def __init__(self, uow: PostgreSQLTokenUnitOfWork):
        self._uow = uow

    async def execute(self, dto: UserLoginDTO):
        async with self._uow as uow_:
            user = await uow_.user_repository.get(dto)
            token = await uow_.token_repository.create(user)
        return token
