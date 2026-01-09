from dataclasses import dataclass


@dataclass
class UserDTO:
    id: int
    username: str
    last_name: str
    first_name: str
    email: str
    is_admin: bool
    patronymic: str | None = None


@dataclass
class UserCreateDTO:
    username: str
    last_name: str
    first_name: str
    email: str
    is_admin: bool
    password: str
    patronymic: str | None = None
