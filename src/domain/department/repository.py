from abc import ABC, abstractmethod

from domain.department.models import DepartmentCreateDTO


class AbstractDepartmentRepository(ABC):
    @abstractmethod
    async def create(self, dto: DepartmentCreateDTO):
        raise NotImplementedError()
    
    @abstractmethod
    async def list(self):
        raise NotImplementedError()
