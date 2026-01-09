from datetime import datetime
from infrastructure.databases.postgresql.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey


class Token(Base):
    __tablename__ = "token"

    id: Mapped[int] = mapped_column(primary_key=True)
    refresh_token: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    access_token: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    refresh_token_expires_in: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    access_token_expires_in: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    user: Mapped['User'] = relationship(back_populates='tokens')
