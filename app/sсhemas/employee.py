from datetime import date
from enum import Enum
from pydantic import Field
from .base import BaseDTO
from fastapi import UploadFile,File


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class EmployeeDTO(BaseDTO):
    id: int | None = None 
    first_name: str | None = None 
    last_name: str | None = None 
    patronymic: str | None = None 
    birth_date: date | None = None
    phone: str | None = None 
    gender: Gender | None = None 
    avatar_url: str | None = None

class EmployeeFilterDTO(BaseDTO):
    page: int
    per_page: int
    search: str | None = None
    gender: Gender | None = None
    age_from: int | None = None
    age_to: int | None = None