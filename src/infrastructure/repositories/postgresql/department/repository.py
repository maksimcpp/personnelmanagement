from typing import Optional
from sqlalchemy import select
from domain.department.models import DepartmentCreateDTO, DepartmentDTO
from domain.department.repository import AbstractDepartmentRepository
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.databases.postgresql.models.department import Department


class PostgreSQLDepartmentRepository(AbstractDepartmentRepository):
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, dto: DepartmentCreateDTO):
        department = Department(
            name=dto.name
        )
        self._session.add(department)
        await self._session.flush()
        return DepartmentDTO(
            id=department.id,
            name=department.name
        )
    
    async def list_departments(
        self, limit: Optional[int] = None, offset: int = 0
    ):
        query = select(Department).offset(offset)
        if limit is not None:
            query = query.limit(limit)

        result = await self._session.execute(query)
        departments = result.scalars().all()
        departments_dto = [
             DepartmentDTO(
                id=department.id,
                name=department.name
            ) for department in departments
        ]
        return departments_dto
