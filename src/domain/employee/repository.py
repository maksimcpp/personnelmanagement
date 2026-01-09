from abc import ABC, abstractmethod

from domain.employee.models import EmployeeCreateDTO, EmployeeFilterDTO
from domain.user.models import UserDTO
from utils.enums import EmployeeStatus


class AbstractEmployeeRepository(ABC):
    @abstractmethod
    async def create(self, dto: EmployeeCreateDTO):
        raise NotImplementedError()
    
    @abstractmethod
    async def set_team(self, team_id: int, employee_id: int):
        raise NotImplementedError()
    
    @abstractmethod
    async def update_status(self, employee_id: int, status: EmployeeStatus):
        raise NotImplementedError()
    
    @abstractmethod
    async def list_employees(self, filter_dto: EmployeeFilterDTO):
        raise NotImplementedError()
    
    @abstractmethod
    async def get_current_employee(self, user_dto: UserDTO):
        raise NotImplementedError()
