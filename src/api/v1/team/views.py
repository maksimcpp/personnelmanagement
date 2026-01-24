from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse

from api.v1.team.dependencies import create_team_use_case, list_team_use_case
from api.v1.team.models import TeamCreateSchema, TeamSchema
from api.v1.user.dependencies import get_current_user
from domain.team.models import TeamCreateDTO, TeamFilterDTO
from domain.user.models import UserDTO
from infrastructure.repositories.postgresql.team.exceptions import InvalidDepartmentId
from usecase.create_team.abstract import AbstractCreateTeamUseCase
from usecase.list_teams.abstract import AbstractListTeamUseCase

router = APIRouter(prefix='/teams')

@router.post("", response_model=TeamSchema)
async def create_team(
    payload: TeamCreateSchema,
    user: UserDTO = Depends(get_current_user),
    use_case: AbstractCreateTeamUseCase = Depends(create_team_use_case)
) -> JSONResponse:
    if not user.is_admin:
        return JSONResponse(
            {'detail': 'User is not a admin.'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    team_create_dto = TeamCreateDTO(
        name=payload.name,
        department_id=payload.department_id
    )
    try:
        new_team_dto = await use_case.execute(team_create_dto)
    except InvalidDepartmentId as e:
        return JSONResponse(
            content={'detail': f'{e}'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    schema = TeamSchema(
        id=new_team_dto.id,
        name=new_team_dto.name,
        department_id=new_team_dto.department_id
    )
    return JSONResponse(
        content=schema.model_dump(),
        status_code=status.HTTP_201_CREATED
    )

@router.get("", response_model=List[TeamSchema])
async def list_teams(
    offset: Optional[int] = Query(None, ge=0),
    limit: Optional[int] = Query(None, ge=0, le=100),
    department_id: Optional[int] = Query(None, ge=0),
    user: UserDTO = Depends(get_current_user),
    use_case: AbstractListTeamUseCase = Depends(list_team_use_case)
) -> JSONResponse:
    if not user.is_admin:
        return JSONResponse(
            {'detail': 'User is not a admin.'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )

    filter_dto = TeamFilterDTO(
        department_id=department_id
    )
    teams_dto = await use_case.execute(
        filter_dto=filter_dto,
        offset=offset,
        limit=limit
    )
    schema = [
        TeamSchema(
            id=team.id,
            name=team.name,
            department_id=team.department_id
        ).model_dump() for team in teams_dto
    ]
    return JSONResponse(
        content=schema,
        status_code=status.HTTP_200_OK
    )
