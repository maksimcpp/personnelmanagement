from abc import ABC, abstractmethod

from domain.employee.models import EmployeeCreateDTO
from domain.user.models import UserCreateDTO


class AbstractCreateEmployeeUseCase(ABC):
    @abstractmethod
    async def execute(
        self, 
        employee_dto: EmployeeCreateDTO,
        user_dto: UserCreateDTO    
    ):
        raise NotImplementedError()
