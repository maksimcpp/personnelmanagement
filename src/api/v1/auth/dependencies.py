from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from infrastructure.databases.postgresql.session import get_session
from infrastructure.repositories.postgresql.token.uow import PostgreSQLTokenUnitOfWork
from usecase.create_token.abstract import AbstractCreateTokenUseCase
from usecase.create_token.implementation import PostgreSQLCreateTokenUseCase
from usecase.delete_token.abstract import AbstractDeleteTokenUseCase
from usecase.delete_token.implementation import PostgreSQLDeleteTokenUseCase
from usecase.refresh_token.abstract import AbstractRefreshTokenUseCase
from usecase.refresh_token.implementation import PostgreSQLRefreshTokenUseCase


def create_token_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractCreateTokenUseCase:
    uow = PostgreSQLTokenUnitOfWork(session)
    return PostgreSQLCreateTokenUseCase(uow)

def refresh_token_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractRefreshTokenUseCase:
    uow = PostgreSQLTokenUnitOfWork(session)
    return PostgreSQLRefreshTokenUseCase(uow)

def delete_token_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractDeleteTokenUseCase:
    uow = PostgreSQLTokenUnitOfWork(session)
    return PostgreSQLDeleteTokenUseCase(uow)
