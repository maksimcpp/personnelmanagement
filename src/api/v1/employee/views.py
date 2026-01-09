from typing import List
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from api.v1.employee.dependencies import create_employee_use_case, get_current_employee_use_case, list_employee_by_status_use_case, list_employee_use_case, set_team_id_use_case, update_employee_status_use_case
from api.v1.employee.models import EmployeeSchema, EmployeeUserCreateSchema, EmployeeUserSchema
from api.v1.user.dependencies import get_current_user
from domain.employee.models import EmployeeCreateDTO, EmployeeFilterDTO, EmployeeUserDTO
from domain.user.models import UserCreateDTO, UserDTO
from infrastructure.repositories.postgresql.employee.exceptions import EmployeeNotActive, EmployeeNotExist, InvalidEmployeeId, InvalidTeamId
from infrastructure.repositories.postgresql.user.exceptions import UserAlreadyExist
from usecase.create_employee.abstract import AbstractCreateEmployeeUseCase
from usecase.get_current_employee.abstract import AbstractGetCurrentEmployeeUseCase
from usecase.list_employees.abstract import AbstractListEmployeesUseCase
from usecase.list_employees_by_status.abstract import AbstractListEmployeesByStatusUseCase
from usecase.set_team_to_employee.abstract import AbstractSetTeamIdUseCase
from usecase.update_employee_status.abstract import AbstractUpdateEmployeeStatusUseCase
from utils.enums import EmployeeStatus

router = APIRouter(prefix='/employees')

@router.post("", response_model=EmployeeUserSchema)
async def create_employee(
    payload: EmployeeUserCreateSchema,
    use_case: AbstractCreateEmployeeUseCase = Depends(create_employee_use_case)
) -> JSONResponse:
    user_dto = UserCreateDTO(
        username=payload.username,
        last_name=payload.last_name,
        first_name=payload.first_name,
        patronymic=payload.patronymic,
        email=payload.email,
        is_admin=payload.is_admin,
        password=payload.password
    )
    employee_dto = EmployeeCreateDTO(
        status=EmployeeStatus.CONSIDERATION
    )
    try:
        employee_user_dto = await use_case.execute(
            employee_dto=employee_dto,
            user_dto=user_dto
        )
    except UserAlreadyExist as e:
        return JSONResponse(
        content={'detail': f'{e}'},
        status_code=status.HTTP_400_BAD_REQUEST
    )

    employee_user_schema = EmployeeUserSchema(
        id=employee_user_dto.id,
        username=employee_user_dto.username,
        last_name=employee_user_dto.last_name,
        first_name=employee_user_dto.first_name,
        patronymic=employee_user_dto.patronymic,
        email=employee_user_dto.email,
        status=employee_user_dto.status,
        is_admin=employee_user_dto.is_admin,
    )
    return JSONResponse(
        content=employee_user_schema.model_dump(mode='json'),
        status_code=status.HTTP_201_CREATED
    )

@router.post("/{employee_id}/status", response_model=EmployeeSchema)
async def update_employee_status(
    employee_id: int,
    employee_status: EmployeeStatus,
    user: UserDTO = Depends(get_current_user),
    use_case: AbstractUpdateEmployeeStatusUseCase = Depends(update_employee_status_use_case)
) -> JSONResponse:
    if not user.is_admin:
        return JSONResponse(
            {'detail': 'User is not a admin.'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        employee_dto = await use_case.execute(
            employee_id=employee_id,
            status=employee_status
        )
    except InvalidEmployeeId as e:
        return JSONResponse(
            {'detail': f'{e}'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    schema = EmployeeSchema(
        id=employee_dto.id,
        status=employee_dto.status,
        user_id=employee_dto.user_id,
        team_id=employee_dto.team_id,
    )
    return JSONResponse(
        schema.model_dump(mode='json'),
        status_code=status.HTTP_202_ACCEPTED
    )

@router.post("/{employee_id}/team/{team_id}", response_model=EmployeeSchema)
async def set_team_id(
    employee_id: int, 
    team_id: int,
    user: UserDTO = Depends(get_current_user),
    use_case: AbstractSetTeamIdUseCase = Depends(set_team_id_use_case)
) -> JSONResponse:
    if not user.is_admin:
        return JSONResponse(
            {'detail': 'User is not a admin.'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    try:
        employee_dto = await use_case.execute(team_id, employee_id)
    except InvalidTeamId as e:
        return JSONResponse(
            {'detail': f'{e}'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except EmployeeNotActive as e:
        return JSONResponse(
            {'detail': f'{e}'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    schema = EmployeeSchema(
        id=employee_dto.id,
        status=employee_dto.status,
        user_id=employee_dto.user_id,
        team_id=employee_dto.team_id,
    )
    return JSONResponse(
        schema.model_dump(mode='json'),
        status_code=status.HTTP_202_ACCEPTED
    )

@router.get("", response_model=List[EmployeeSchema])
async def list_employees(
    team_id: int = Query(None, gt=0),
    department_id: int = Query(None, gt=0),
    employee_status: EmployeeStatus = Query(None),
    user: UserDTO = Depends(get_current_user),
    use_case: AbstractListEmployeesUseCase = Depends(list_employee_use_case)
) -> JSONResponse:
    if not user.is_admin:
        return JSONResponse(
            {'detail': 'User is not a admin.'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    filter_dto = EmployeeFilterDTO(
        team_id=team_id,
        status=employee_status,
        department_id=department_id
    )
    employees = await use_case.execute(filter_dto)
    
    schema = [
        EmployeeSchema(
            id=employee.id,
            status=employee.status,
            user_id=employee.user_id,
            team_id=employee.team_id,
        ).model_dump(mode='json') for employee in employees
    ]

    return JSONResponse(
        content=schema,
        status_code=status.HTTP_202_ACCEPTED
    )

@router.get("/me", response_model=EmployeeUserSchema)
async def get_current_user(
    user: UserDTO = Depends(get_current_user),
    use_case: AbstractGetCurrentEmployeeUseCase = Depends(get_current_employee_use_case)
) -> JSONResponse:
    try:
        employee_user_dto = await use_case.execute(user)
    except EmployeeNotExist as e:
        return JSONResponse(
            {'detail': f'{e}'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    employee_user_schema = EmployeeUserSchema(
        id=employee_user_dto.id,
        username=employee_user_dto.username,
        last_name=employee_user_dto.last_name,
        first_name=employee_user_dto.first_name,
        patronymic=employee_user_dto.patronymic,
        email=employee_user_dto.email,
        status=employee_user_dto.status,
        team_id=employee_user_dto.team_id,
        is_admin=employee_user_dto.is_admin,
    )
    return JSONResponse(
        content=employee_user_schema.model_dump(mode='json'),
        status_code=status.HTTP_201_CREATED
    )
