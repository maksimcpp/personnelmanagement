from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from domain.token.models import AccessTokenDTO
from domain.user.models import UserDTO
from infrastructure.databases.postgresql.models import Token, User
from infrastructure.databases.postgresql.session import get_session
from infrastructure.repositories.postgresql.token.exceptions import TokenLifetimeExpired, TokenNotExist
from infrastructure.repositories.postgresql.token.uow import PostgreSQLTokenUnitOfWork
from infrastructure.repositories.postgresql.user.exceptions import UserNotExist
from infrastructure.repositories.postgresql.user.uow import PostgreSQLUserUnitOfWork
from usecase.create_user.abstract import AbstractCreateUserUseCase
from usecase.create_user.implementation import PostgreSQLCreateUserUseCase
from usecase.get_user.abstract import AbstractGetUserUseCase
from usecase.get_user.implementation import PostgreSQLGetUserUseCase
from .bearer import oauth2_scheme

def create_user_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractCreateUserUseCase:
    uow = PostgreSQLUserUnitOfWork(session)
    return PostgreSQLCreateUserUseCase(uow)

def get_user_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractGetUserUseCase:
    uow = PostgreSQLTokenUnitOfWork(session)
    return PostgreSQLGetUserUseCase(uow)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    use_case: PostgreSQLGetUserUseCase = Depends(get_user_use_case)
) -> UserDTO:
    token_dto = AccessTokenDTO(
        access_token=credentials.credentials
    )
    try:
        user_dto = await use_case.execute(token_dto)
    except TokenNotExist as e:
        raise HTTPException(
            detail=f'{e}',
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except TokenLifetimeExpired as e:
        raise HTTPException(
            detail=f'{e}',
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except UserNotExist as e:
        raise HTTPException(
            detail=f'{e}',
            status_code=status.HTTP_400_BAD_REQUEST
        )
    return user_dto
    