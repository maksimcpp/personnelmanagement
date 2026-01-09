from dataclasses import dataclass


@dataclass
class TeamDTO:
    id: int
    name: str
    department_id: int


@dataclass
class TeamCreateDTO:
    name: str
    department_id: int


@dataclass
class TeamRenameDTO:
    name: str
