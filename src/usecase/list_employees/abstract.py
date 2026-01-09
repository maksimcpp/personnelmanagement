from abc import ABC, abstractmethod

from domain.employee.models import EmployeeFilterDTO


class AbstractListEmployeesUseCase(ABC):
    @abstractmethod
    async def execute(self, filter_dto: EmployeeFilterDTO):
        raise NotImplementedError()
