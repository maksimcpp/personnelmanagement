from abc import ABC, abstractmethod


class AbstractListDepartmentUseCase(ABC):
    @abstractmethod
    async def execute(self):
        raise NotImplementedError()
