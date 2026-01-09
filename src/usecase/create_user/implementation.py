from domain.user.models import UserCreateDTO
from infrastructure.repositories.postgresql.user.uow import PostgreSQLUserUnitOfWork
from usecase.create_user.abstract import AbstractCreateUserUseCase


class PostgreSQLCreateUserUseCase(AbstractCreateUserUseCase):
    def __init__(self, uow: PostgreSQLUserUnitOfWork):
        self._uow = uow

    async def execute(self, dto: UserCreateDTO):
        async with self._uow as uow_:
            user = await uow_.repository.create(dto)
        return user
