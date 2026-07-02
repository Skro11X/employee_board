import logging
from typing import Annotated, List
from fastapi import APIRouter, UploadFile, File, Depends, Form, Query
from pydantic import Json
from api.dependencies import get_employee_service
from api.serializer import PaginateParams, EmployeeFilterParams, EmployeesResponse
from schemas import EmployeeFilterDTO
from contracts import EmployeesServiceProtocol



logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/employee/")
async def get_employee(
    employee_service: Annotated[EmployeesServiceProtocol, Depends(get_employee_service)],
    paginate: PaginateParams = Depends(),
    filters: EmployeeFilterParams = Depends(),
):
    employees, count = employee_service.get_list(
        EmployeeFilterDTO(
            **paginate.model_dump(),
            **filters.model_dump(),
        )         
    )

    return EmployeesResponse(
        items = employees,
        count = count,
        page = paginate.page,
        per_page = paginate.per_page,
    )


@router.post("/employees/")
async def create_employee(
    
):
    pass


@router.put("/employee/{uuid}")
async def put_employee(
    
):
    return 

@router.delete("/employee/{uuid}")
async def delete_employee(
    
):
    return 