from typing import Optional
from infrastructure.databases.postgresql.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum, ForeignKey

from utils.enums import EmployeeStatus


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(primary_key=True)
    status: Mapped[EmployeeStatus] = mapped_column(Enum(EmployeeStatus), nullable=False)
    team_id: Mapped[Optional[int]] = mapped_column(ForeignKey('team.id'), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    user: Mapped['User'] = relationship(back_populates='employee')
    team: Mapped[Optional['Team']] = relationship(back_populates='employee')
