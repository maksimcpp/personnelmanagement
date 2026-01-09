from sqlalchemy import select
from domain.token.models import UserLoginDTO
from domain.user.models import UserCreateDTO, UserDTO
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domain.user.repository import AbstractUserRepository
from infrastructure.databases.postgresql.models.user import User
from infrastructure.repositories.postgresql.token.exceptions import InvalidPassword, InvalidUsername
from infrastructure.repositories.postgresql.user.exceptions import UserAlreadyExist
from .crypt import context


class PostgreSQLUserRepository(AbstractUserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, dto: UserCreateDTO):
        user = User(
            username=dto.username,
            last_name=dto.last_name,
            first_name=dto.first_name,
            patronymic=dto.patronymic,
            email=dto.email,
            is_admin=dto.is_admin,
            password=context.hash(dto.password)
        )
        self._session.add(user)
        try:
            await self._session.flush()
        except IntegrityError:
            raise UserAlreadyExist()
        
        return UserDTO(
            id=user.id,
            username=user.username,
            last_name=user.last_name,
            first_name=user.first_name,
            patronymic=user.patronymic,
            email=user.email,
            is_admin=dto.is_admin,
        )

    async def get(self, dto: UserLoginDTO):
        query = select(User).where(
            User.username == dto.username
        )
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()

        if not user:
            raise InvalidUsername()

        verify = context.verify(dto.password, user.password)

        if not verify:
            raise InvalidPassword()
        
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            last_name=user.last_name,
            first_name=user.first_name,
            patronymic=user.patronymic,
            is_admin=user.is_admin,
        )
