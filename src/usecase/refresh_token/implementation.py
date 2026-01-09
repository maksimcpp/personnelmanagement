from domain.token.models import RefreshTokenDTO
from infrastructure.repositories.postgresql.token.uow import PostgreSQLTokenUnitOfWork
from usecase.refresh_token.abstract import AbstractRefreshTokenUseCase


class PostgreSQLRefreshTokenUseCase(AbstractRefreshTokenUseCase):
    def __init__(self, uow: PostgreSQLTokenUnitOfWork):
        self._uow = uow

    async def execute(self, dto: RefreshTokenDTO):
        async with self._uow as uow_:
            token = await uow_.token_repository.refresh(dto)
        return token
