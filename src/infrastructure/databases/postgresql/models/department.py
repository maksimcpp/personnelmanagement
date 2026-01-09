from typing import List
from infrastructure.databases.postgresql.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


class Department(Base):
    __tablename__ = "department"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    teams: Mapped[List['Team']] = relationship(back_populates='department')
