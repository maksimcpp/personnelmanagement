from pydantic import BaseModel


class TeamSchema(BaseModel):
    id: int
    name: str
    department_id: int



class TeamCreateSchema(BaseModel):
    name: str
    department_id: int



class TeamRenameSchema(BaseModel):
    name: str