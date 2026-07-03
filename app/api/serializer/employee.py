from datetime import date
from pydantic import Field, ConfigDict
from sсhemas import BaseRequest, Gender, BaseResponse, EmployeeDTO

class PaginateParams(BaseRequest):
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=10, ge=1, le=100)


class EmployeeFilterParams(BaseRequest):
    search: str | None = None
    gender: Gender | None = None
    age_from: int | None = Field(default=None, ge=0)
    age_to: int | None = Field(default=None, le=150)


class EmployeeResponse(BaseResponse):
    id: int
    first_name: str
    last_name: str
    patronymic: str | None = None 
    birth_date: date | None = None
    phone: str
    gender: Gender 
    avatar_url: str | None = None
    model_config = ConfigDict(from_attributes=True)


class EmployeesResponse(BaseResponse):
    items: list[EmployeeResponse] 
    count: int
    page: int
    per_page: int
    


class EmployeeCreateRequest(BaseRequest):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    patronymic: str | None = None
    birth_date: date | None = None
    phone: str = Field(..., min_length=5)
    gender: Gender


class EmployeeUpdateRequest(BaseRequest):
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    patronymic: str | None = None
    birth_date: date | None = None
    phone: str = Field(..., min_length=5)
    gender: Gender
    avatar_url: str | None = None
