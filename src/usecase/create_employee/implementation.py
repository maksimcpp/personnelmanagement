from domain.employee.models import EmployeeCreateDTO, EmployeeDTO, EmployeeUserDTO
from domain.user.models import UserCreateDTO, UserDTO
from infrastructure.repositories.postgresql.employee.uow import PostgreSQLEmployeeUnitOfWork
from usecase.create_employee.abstract import AbstractCreateEmployeeUseCase


class PostgreSQLCreateEmployeeUseCase(AbstractCreateEmployeeUseCase):
    def __init__(self, uow: PostgreSQLEmployeeUnitOfWork):
        self._uow = uow

    async def execute(
        self, 
        employee_dto: EmployeeCreateDTO,
        user_dto: UserCreateDTO    
    ):
        async with self._uow as uow_:
            user: UserDTO = await uow_.user_repository.create(user_dto)
            employee_dto.user_id = user.id
            employee: EmployeeDTO = await uow_.employee_repository.create(employee_dto)
    
        return EmployeeUserDTO(
            id=employee.id,
            username=user.username,
            last_name=user.last_name,
            first_name=user.first_name,
            patronymic=user.patronymic,
            email=user.email,
            status=employee.status,
            is_admin=user.is_admin,
        )
