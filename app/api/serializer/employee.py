from pydantic import Field
from schemas import BaseRequest, Gender, BaseResponse, EmployeesDTO


class PaginateParams(BaseRequest):
    page: int = Field(default=1, ge=1)
    per_page: int = Field(default=10, ge=1, le=100)


class EmployeeFilterParams(BaseRequest):
    search: str | None = None
    gender: list[Gender] | None = None
    age_from: int | None = Field(default=None, ge=0)
    age_to: int | None = Field(default=None, le=150)


class EmployeesResponse(BaseResponse):
    items: list[EmployeesDTO]
    count: int
    page: int
    per_page: int