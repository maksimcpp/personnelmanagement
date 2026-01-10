from pydantic import BaseModel, EmailStr

from utils.enums import EmployeeStatus


class EmployeeUserSchema(BaseModel):
    id: int
    status: EmployeeStatus
    username: str
    last_name: str
    first_name: str
    email: EmailStr
    is_admin: bool
    patronymic: str | None = None
    team_id: int | None = None


class EmployeeUserCreateSchema(BaseModel):
    username: str
    last_name: str
    first_name: str
    email: EmailStr
    password: str
    patronymic: str | None = None


class EmployeeTeamSchema(BaseModel):
    team_id: int


class EmployeeSchema(BaseModel):
    id: int
    status: EmployeeStatus
    user_id: int
    team_id: int | None = None


class EmployeeCreateSchema(BaseModel):
    status: EmployeeStatus
    user_id: int
    team_id: int | None = None
