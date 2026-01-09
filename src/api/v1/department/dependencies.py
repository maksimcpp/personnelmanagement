from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from infrastructure.databases.postgresql.session import get_session
from infrastructure.repositories.postgresql.department.uow import PostgreSQLDepartmentUnitOfWork
from usecase.create_department.abstract import AbstractCreateDepartmentUseCase
from usecase.create_department.implementation import PostgreSQLCreateDepartmentUseCase
from usecase.list_departments.abstract import AbstractListDepartmentUseCase
from usecase.list_departments.implementation import PostgreSQLListDepartmentUseCase


def create_department_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractCreateDepartmentUseCase:
    uow = PostgreSQLDepartmentUnitOfWork(session)
    return PostgreSQLCreateDepartmentUseCase(uow)

def list_department_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractListDepartmentUseCase:
    uow = PostgreSQLDepartmentUnitOfWork(session)
    return PostgreSQLListDepartmentUseCase(uow)
    