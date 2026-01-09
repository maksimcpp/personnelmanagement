from abc import ABC, abstractmethod

from utils.enums import EmployeeStatus


class AbstractListEmployeesByStatusUseCase(ABC):
    @abstractmethod
    async def execute(self, employee_status: EmployeeStatus):
        raise NotImplementedError()
