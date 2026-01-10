from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    last_name: str
    first_name: str
    email: EmailStr
    is_admin: bool
    patronymic: str | None = None


class UserCreateSchema(BaseModel):
    username: str
    last_name: str
    first_name: str
    email: EmailStr
    password: str
    patronymic: str | None = None
