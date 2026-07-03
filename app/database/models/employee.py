from datetime import date
from sqlalchemy import String, Date, Enum as SQLEnum, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from database.models.base import Base, int_pk
from sсhemas.employee import Gender

class Employee(Base):
    id: Mapped[int_pk]
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    patronymic: Mapped[str | None] = mapped_column(String(100), nullable=True)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    gender: Mapped[Gender] = mapped_column(SQLEnum(Gender), default=Gender.MALE, nullable=False)
    avatar_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)