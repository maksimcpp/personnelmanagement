from abc import ABC, abstractmethod


class AbstractSetTeamIdUseCase(ABC):
    @abstractmethod
    async def execute(self, team_id: int, employee_id: int):
        raise NotImplementedError()
