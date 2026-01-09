from abc import ABC, abstractmethod

from domain.department.models import DepartmentCreateDTO


class AbstractCreateDepartmentUseCase(ABC):
    @abstractmethod
    async def execute(self, dto: DepartmentCreateDTO):
        raise NotImplementedError()
