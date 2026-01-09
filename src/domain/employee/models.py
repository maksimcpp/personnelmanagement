from dataclasses import dataclass

from utils.enums import EmployeeStatus


@dataclass
class EmployeeUserDTO:
    id: int
    status: EmployeeStatus
    username: str
    last_name: str
    first_name: str
    email: str
    is_admin: bool
    patronymic: str | None = None
    team_id: int | None = None


@dataclass
class EmployeeTeanDTO:
    team_id: int


@dataclass
class EmployeeDTO:
    id: int
    status: EmployeeStatus
    user_id: int
    team_id: int | None = None


@dataclass
class EmployeeCreateDTO:
    status: EmployeeStatus
    user_id: int | None = None
    team_id: int | None = None


@dataclass
class EmployeeFilterDTO:
    status: EmployeeStatus | None = None
    team_id: int | None = None
    department_id: int | None = None
