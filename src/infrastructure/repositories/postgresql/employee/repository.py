from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from domain.employee.models import EmployeeCreateDTO, EmployeeDTO, EmployeeFilterDTO, EmployeeUserDTO
from domain.employee.repository import AbstractEmployeeRepository
from domain.user.models import UserDTO
from infrastructure.databases.postgresql.models.employee import Employee
from infrastructure.databases.postgresql.models.team import Team
from infrastructure.repositories.postgresql.employee.exceptions import EmployeeNotActive, EmployeeNotExist, InvalidEmployeeId, InvalidTeamId
from utils.enums import EmployeeStatus


class PostgreSQLEmployeeRepository(AbstractEmployeeRepository):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, dto: EmployeeCreateDTO):
        employee = Employee(
            status=EmployeeStatus.CONSIDERATION,
            user_id=dto.user_id,
        )
        self._session.add(employee)
        await self._session.flush()
        employee_dto = EmployeeDTO(
            id=employee.id,
            status=employee.status,
            user_id=employee.user_id,
        )
        return employee_dto
    
    async def set_team(self, team_id: int, employee_id: int):
        query = select(Employee).where(
            Employee.id == employee_id
        )
        result = await self._session.execute(query)
        employee = result.scalar_one_or_none()
        if employee.status != EmployeeStatus.ACTIVE:
            raise EmployeeNotActive()
        
        employee.team_id = team_id
        self._session.add(employee)

        try:
            await self._session.flush()
        except IntegrityError:
            raise InvalidTeamId()
        
        employee_dto = EmployeeDTO(
            id=employee.id,
            status=employee.status,
            user_id=employee.user_id,
            team_id=employee.team_id,
        )
        return employee_dto
    
    async def update_status(self, employee_id: int, status: EmployeeStatus):
        query = select(Employee).where(
            Employee.id == employee_id
        )
        result = await self._session.execute(query)
        employee = result.scalar_one_or_none()
        employee.status = status
        self._session.add(employee)
        try:
            await self._session.flush()
        except IntegrityError:
            raise InvalidEmployeeId()
        
        return EmployeeDTO(
            id=employee.id,
            status=employee.status,
            user_id=employee.user_id,
            team_id=employee.team_id,
        )
    
    async def list_employees(self, filter_dto: EmployeeFilterDTO):
        query = select(Employee)
        filters = []
        if filter_dto.status:
            filters.append(Employee.status == filter_dto.status)

        if filter_dto.team_id:
            filters.append(Employee.team_id == filter_dto.team_id)

        if filter_dto.department_id:
            query = query.join(Team, Employee.team_id == Team.id)
            filters.append(Team.department_id == filter_dto.department_id)

        if filters:
            query = query.where(
                and_(*filters)
            )
        
        query = query.order_by(Employee.id)
        result = await self._session.execute(query)
        
        employees = result.scalars().all()
        employees_dto = [
            EmployeeDTO(
                id=employee.id,
                status=employee.status,
                user_id=employee.user_id,
                team_id=employee.team_id,
            ) for employee in employees
        ]
        return employees_dto
    
    async def get_current_employee(self, user_dto: UserDTO):
        query = select(Employee).where(
            Employee.user_id == user_dto.id
        )
        result = await self._session.execute(query)
        employee = result.scalar_one_or_none()
        if employee is None:
            raise EmployeeNotExist()
        
        return EmployeeUserDTO(
            id=employee.id,
            username=user_dto.username,
            last_name=user_dto.last_name,
            first_name=user_dto.first_name,
            patronymic=user_dto.patronymic,
            email=user_dto.email,
            status=employee.status,
            team_id=employee.team_id,
            is_admin=user_dto.is_admin,
        )
