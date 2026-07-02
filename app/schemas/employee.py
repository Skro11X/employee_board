from datetime import date
from enum import Enum
from pydantic import Field 
from .base import BaseDTO


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class EmployeeDTO(BaseDTO):
    id: int
    first_name: str
    last_name: str
    patronymic: str | None = None 
    birth_date: date | None = None
    phone: str
    gender: Gender 
    avatar_url: str | None = None
    # deleted


class EmployeeFilterDTO(BaseDTO):
    page: int
    per_page: int
    search: str | None = None
    gender: list[Gender] | None = None
    age_from: str | None = None
    age_to: str | None = None

    