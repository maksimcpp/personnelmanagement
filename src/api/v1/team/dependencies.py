from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from infrastructure.databases.postgresql.session import get_session
from infrastructure.repositories.postgresql.team.uow import PostgreSQLTeamUnitOfWork
from usecase.create_team.abstract import AbstractCreateTeamUseCase
from usecase.create_team.implementation import PostgreSQLCreateTeamUseCase
from usecase.list_teams.abstract import AbstractListTeamUseCase
from usecase.list_teams.implementation import PostgreSQLListTeamUseCase


def create_team_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractCreateTeamUseCase:
    uow = PostgreSQLTeamUnitOfWork(session)
    return PostgreSQLCreateTeamUseCase(uow)

def list_team_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractListTeamUseCase:
    uow = PostgreSQLTeamUnitOfWork(session)
    return PostgreSQLListTeamUseCase(uow)
