from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials

from api.v1.auth.models import AccessTokenSchema
from api.v1.user.dependencies import create_user_use_case, get_user_use_case
from api.v1.user.models import UserCreateSchema, UserSchema
from domain.token.models import AccessTokenDTO
from domain.user.models import UserCreateDTO, UserDTO
from infrastructure.repositories.postgresql.token.exceptions import TokenLifetimeExpired, TokenNotExist
from infrastructure.repositories.postgresql.user.exceptions import UserAlreadyExist, UserNotExist
from usecase.create_user.implementation import PostgreSQLCreateUserUseCase
from usecase.get_user.abstract import AbstractGetUserUseCase
from .bearer import oauth2_scheme

router = APIRouter(prefix='/users')

@router.post("", response_model=UserSchema)
async def create_user(
    payload: UserCreateSchema,
    use_case: PostgreSQLCreateUserUseCase = Depends(create_user_use_case)
) -> JSONResponse:
    user_create_dto = UserCreateDTO(
        username=payload.username,
        last_name=payload.last_name,
        first_name=payload.first_name,
        patronymic=payload.patronymic,
        email=payload.email,
        is_admin=True,
        password=payload.password
    )
    try:
        created_user_dto: UserDTO = await use_case.execute(user_create_dto)
    except UserAlreadyExist as e:
        return JSONResponse(
        content={'detail': f'{e}'},
        status_code=status.HTTP_400_BAD_REQUEST
    )

    schema = UserSchema(
        id=created_user_dto.id,
        username=created_user_dto.username,
        last_name=created_user_dto.last_name,
        first_name=created_user_dto.first_name,
        patronymic=created_user_dto.patronymic,
        email=created_user_dto.email,
        is_admin=created_user_dto.is_admin,
    )
    return JSONResponse(
        content=schema.model_dump(),
        status_code=status.HTTP_201_CREATED
    )

@router.get("/me", response_model=UserDTO)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    use_case: AbstractGetUserUseCase = Depends(get_user_use_case)
) -> JSONResponse:
    token_dto = AccessTokenDTO(
        access_token=credentials.credentials
    )
    try:
        user = await use_case.execute(token_dto)
    except TokenNotExist as e:
        return JSONResponse(
            {'detail': f'{e}'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except TokenLifetimeExpired as e:
        return JSONResponse(
            {'detail': f'{e}'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    except UserNotExist as e:
        return JSONResponse(
            {'detail': f'{e}'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    user_schema = UserSchema(
        id=user.id,
        username=user.username,
        last_name=user.last_name,
        first_name=user.first_name,
        patronymic=user.patronymic,
        email=user.email,
        is_admin=user.is_admin,
    )
    return JSONResponse(
        user_schema.model_dump(),
        status_code=status.HTTP_200_OK
    )
