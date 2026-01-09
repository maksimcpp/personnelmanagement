from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials

from api.v1.auth.dependencies import create_token_use_case, delete_token_use_case, refresh_token_use_case
from api.v1.auth.models import RefreshTokenSchema, TokenSchema, UserLoginSchema
from api.v1.department.dependencies import create_department_use_case
from api.v1.department.models import DepartmentSchema, DepartmentCreateSchema
from api.v1.user.dependencies import get_current_user
from api.v1.user.bearer import oauth2_scheme
from domain.department.models import DepartmentCreateDTO
from domain.token.models import AccessTokenDTO, RefreshTokenDTO, UserLoginDTO
from domain.user.models import UserDTO
from infrastructure.repositories.postgresql.token.exceptions import InvalidPassword, InvalidUsername, TokenLifetimeExpired, TokenNotExist
from usecase.create_department.abstract import AbstractCreateDepartmentUseCase
from usecase.create_token.abstract import AbstractCreateTokenUseCase
from usecase.delete_token.abstract import AbstractDeleteTokenUseCase
from usecase.refresh_token.abstract import AbstractRefreshTokenUseCase

router = APIRouter(prefix='/auth')

@router.post("/token", response_model=TokenSchema)
async def create_token(
    payload: UserLoginSchema,
    use_case: AbstractCreateTokenUseCase = Depends(create_token_use_case)
) -> JSONResponse:
    user_login_dto = UserLoginDTO(
        username=payload.username,
        password=payload.password
    )
    try:
        token_dto = await use_case.execute(user_login_dto)
    except InvalidUsername as e:
        return JSONResponse(
            {'detail': f'{e}'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    except InvalidPassword as e:
        return JSONResponse(
            {'detail': f'{e}'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    schema =  TokenSchema(
        access_token=token_dto.access_token,
        refresh_token=token_dto.refresh_token,
        access_token_expires_in=token_dto.access_token_expires_in,
        refresh_token_expires_in=token_dto.refresh_token_expires_in
    )
    return JSONResponse(
        schema.model_dump(mode='json'),
        status_code=status.HTTP_201_CREATED
    )

@router.post("/refresh", response_model=TokenSchema)
async def refresh_token(
    payload: RefreshTokenSchema,
    use_case: AbstractRefreshTokenUseCase = Depends(refresh_token_use_case)
) -> JSONResponse:
    refresh_token_dto = RefreshTokenDTO(
        refresh_token=payload.refresh_token
    )
    try:
        token_dto = await use_case.execute(refresh_token_dto)
    except TokenLifetimeExpired as e:
        return JSONResponse(
            {'detail': f'{e}'},
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    schema =  TokenSchema(
        access_token=token_dto.access_token,
        refresh_token=token_dto.refresh_token,
        access_token_expires_in=token_dto.access_token_expires_in,
        refresh_token_expires_in=token_dto.refresh_token_expires_in
    )
    return JSONResponse(
        schema.model_dump(mode='json'),
        status_code=status.HTTP_201_CREATED
    )

@router.delete("/logout")
async def logout(
    user: UserDTO = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme),
    use_case: AbstractDeleteTokenUseCase = Depends(delete_token_use_case)
) -> JSONResponse:
    token_dto = AccessTokenDTO(
        access_token=credentials.credentials
    )
    try:
        await use_case.execute(token_dto)
    except TokenNotExist as e:
        return JSONResponse(
            {'detail': f'{e}'},
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    return JSONResponse(
        {}, status_code=status.HTTP_202_ACCEPTED
    )
