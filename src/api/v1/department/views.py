from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from api.v1.department.dependencies import create_department_use_case, list_department_use_case
from api.v1.department.models import DepartmentSchema, DepartmentCreateSchema
from api.v1.user.dependencies import get_current_user
from domain.department.models import DepartmentCreateDTO
from domain.user.models import UserDTO
from infrastructure.repositories.postgresql.user.exceptions import UserNotAdmin
from usecase.create_department.abstract import AbstractCreateDepartmentUseCase
from usecase.list_departments.abstract import AbstractListDepartmentUseCase

router = APIRouter(prefix='/departments')

@router.post("", response_model=DepartmentSchema)
async def create_department(
    payload: DepartmentCreateSchema,
    user: UserDTO = Depends(get_current_user),
    use_case: AbstractCreateDepartmentUseCase = Depends(create_department_use_case)
) -> JSONResponse:
    if not user.is_admin:
        return JSONResponse(
            {'detail': 'User is not a admin.'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    department_create_dto = DepartmentCreateDTO(
        name=payload.name
    )
    department_dto = await use_case.execute(department_create_dto)
    schema = DepartmentSchema(
        id=department_dto.id,
        name=department_dto.name
    )
    return JSONResponse(
        content=schema.model_dump(),
        status_code=status.HTTP_201_CREATED
    )

@router.get("", response_model=List[DepartmentSchema])
async def list_departments(
    offset: Optional[int] = Query(None, ge=0),
    limit: Optional[int] = Query(None, ge=0, le=100),
    user: UserDTO = Depends(get_current_user),
    use_case: AbstractListDepartmentUseCase = Depends(list_department_use_case)
) -> JSONResponse:
    if not user.is_admin:
        return JSONResponse(
            {'detail': 'User is not a admin.'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    departments_dto = await use_case.execute(offset, limit)
    departments_schema = [
        DepartmentSchema(
            id=department.id,
            name=department.name
        ).model_dump() for department in departments_dto
    ]
    return JSONResponse(
        content=departments_schema,
        status_code=status.HTTP_200_OK
    )
