from abc import ABC, abstractmethod

from utils.enums import EmployeeStatus


class AbstractUpdateEmployeeStatusUseCase(ABC):
    @abstractmethod
    async def execute(self, employee_id: int, status: EmployeeStatus):
        raise NotImplementedError()
