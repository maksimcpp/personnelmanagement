from dataclasses import dataclass


@dataclass
class DepartmentDTO:
    id: int
    name: str


@dataclass
class DepartmentCreateDTO:
    name: str
