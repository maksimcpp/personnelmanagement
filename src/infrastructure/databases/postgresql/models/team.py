from typing import List
from infrastructure.databases.postgresql.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey


class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    department_id: Mapped[int] = mapped_column(ForeignKey('department.id'), nullable=False)

    department: Mapped['Department'] = relationship(back_populates='teams')
    employee: Mapped[List['Employee']] = relationship(back_populates='team')
