from domain.employee.models import EmployeeCreateDTO, EmployeeDTO, EmployeeUserDTO
from domain.user.models import UserCreateDTO, UserDTO
from infrastructure.repositories.postgresql.employee.uow import PostgreSQLEmployeeUnitOfWork
from usecase.get_current_employee.abstract import AbstractGetCurrentEmployeeUseCase


class PostgreSQLGetCurrentEmployeeUseCase(AbstractGetCurrentEmployeeUseCase):
    def __init__(self, uow: PostgreSQLEmployeeUnitOfWork):
        self._uow = uow

    async def execute(
        self, 
        user_dto: UserDTO    
    ):
        async with self._uow as uow_:
            employee_user_dto = await uow_.employee_repository.get_current_employee(user_dto)
        return employee_user_dto
