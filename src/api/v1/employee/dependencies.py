from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.session import get_session
from infrastructure.repositories.postgresql.employee.uow import PostgreSQLEmployeeUnitOfWork
from usecase.create_employee.abstract import AbstractCreateEmployeeUseCase
from usecase.create_employee.implementation import PostgreSQLCreateEmployeeUseCase
from usecase.get_current_employee.abstract import AbstractGetCurrentEmployeeUseCase
from usecase.get_current_employee.implementation import PostgreSQLGetCurrentEmployeeUseCase
from usecase.list_employees.abstract import AbstractListEmployeesUseCase
from usecase.list_employees.implementation import PostgreSQLListEmployeesUseCase
from usecase.list_employees_by_status.abstract import AbstractListEmployeesByStatusUseCase
from usecase.list_employees_by_status.implementation import PostgreSQLListEmployeesByStatusUseCase
from usecase.set_team_to_employee.abstract import AbstractSetTeamIdUseCase
from usecase.set_team_to_employee.implementation import PostgreSQLSetTeamIdUseCase
from usecase.update_employee_status.abstract import AbstractUpdateEmployeeStatusUseCase
from usecase.update_employee_status.implementation import PostgreSQLUpdateEmployeeStatusUseCase


def create_employee_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractCreateEmployeeUseCase:
    uow = PostgreSQLEmployeeUnitOfWork(session)
    return PostgreSQLCreateEmployeeUseCase(uow)

def set_team_id_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractSetTeamIdUseCase:
    uow = PostgreSQLEmployeeUnitOfWork(session)
    return PostgreSQLSetTeamIdUseCase(uow)

def list_employee_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractListEmployeesUseCase:
    uow = PostgreSQLEmployeeUnitOfWork(session)
    return PostgreSQLListEmployeesUseCase(uow)

def list_employee_by_status_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractListEmployeesByStatusUseCase:
    uow = PostgreSQLEmployeeUnitOfWork(session)
    return PostgreSQLListEmployeesByStatusUseCase(uow)

def update_employee_status_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractUpdateEmployeeStatusUseCase:
    uow = PostgreSQLEmployeeUnitOfWork(session)
    return PostgreSQLUpdateEmployeeStatusUseCase(uow)

def get_current_employee_use_case(
    session: AsyncSession = Depends(get_session)
) -> AbstractGetCurrentEmployeeUseCase:
    uow = PostgreSQLEmployeeUnitOfWork(session)
    return PostgreSQLGetCurrentEmployeeUseCase(uow)
