from typing import List
from infrastructure.databases.postgresql.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    patronymic: Mapped[str] = mapped_column(String(100), nullable=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    tokens: Mapped[List["Token"]] = relationship(
        back_populates='user',
        cascade='all, delete, delete-orphan'
    )
    employee: Mapped["Employee"] = relationship(back_populates='user')
