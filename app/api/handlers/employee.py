import logging
from typing import Annotated
from fastapi import ( 
    APIRouter, 
    Depends, 
    HTTPException, 
    status, 
    Request, 
    Form, 
    UploadFile, 
    File
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import Json 

from core import settings
from api.dependencies import get_employee_service, get_file_service
from api.serializer import PaginateParams, EmployeeFilterParams, EmployeesResponse, EmployeeCreateRequest, EmployeeResponse, EmployeeUpdateRequest
from sсhemas import EmployeeFilterDTO, EmployeeDTO
from contracts import EmployeesServiceProtocol, FileServiceProtocol

logger = logging.getLogger("employee_board")

web_router = APIRouter()

templates = Jinja2Templates(directory=settings.TEMPLATES_DIR)

@web_router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index_page(request: Request):
    return templates.TemplateResponse(request, "index.html")

api_router = APIRouter()

@api_router.get("/employees/", response_model=EmployeesResponse)
async def get_employee(
    employee_service: Annotated[EmployeesServiceProtocol, Depends(get_employee_service)],
    paginate: PaginateParams = Depends(),
    filters: EmployeeFilterParams = Depends(),
):
    employees, count = await employee_service.get_list(
        EmployeeFilterDTO(
            page=paginate.page,
            per_page=paginate.per_page,
            search=filters.search,
            gender=filters.gender,
            age_from=filters.age_from,
            age_to=filters.age_to,
        )         
    )

    return EmployeesResponse(
        items=employees,
        count=count,
        page=paginate.page,
        per_page=paginate.per_page,
    )

@api_router.post("/employees/", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee_service: Annotated[EmployeesServiceProtocol, Depends(get_employee_service)],
    file_service: Annotated[FileServiceProtocol, Depends(get_file_service)],
    form_data: Annotated[Json[EmployeeCreateRequest], Form()],
    file: UploadFile | None = File(None),
):
    employee = EmployeeDTO(
        **form_data.model_dump(),
    )
    if file:
        employee.avatar_url = str(await file_service.save_file_and_get_path(file.filename, file.file))   
    try:
        new_employee = await employee_service.create(employee)
    except:
        await file_service.delete_file(employee.avatar_url)
        return HTMLResponse(status_code=404)
    
    return EmployeeResponse(**new_employee.model_dump())


@api_router.put("/employees/{employee_id}", response_model=EmployeeResponse)
async def put_employee(
    employee_service: Annotated[EmployeesServiceProtocol, Depends(get_employee_service)],
    file_service: Annotated[FileServiceProtocol, Depends(get_file_service)],
    employee_id: int,
    form_data: Annotated[Json[EmployeeUpdateRequest], Form()],
    file: UploadFile | None = File(None),
):
    employee = EmployeeDTO(
        **form_data.model_dump(),
    )
    
    old_file_path = employee.avatar_url 
    employee.avatar_url = None
    if file:
        employee.avatar_url = str(await file_service.save_file_and_get_path(file.filename, file.file)) 
    try:
        new_employee = await employee_service.update(employee_id, employee)
    except Exception as e:
        await file_service.delete_file(employee.avatar_url)
        raise HTTPException(status_code=404, detail=f"Employee not found {e}",)
    if old_file_path:
        await file_service.delete_file(old_file_path)

    return EmployeeResponse(**new_employee.model_dump())


@api_router.delete("/employees/{employee_id}")
async def delete_employee(
    employee_id: int,
    employee_service: Annotated[EmployeesServiceProtocol, Depends(get_employee_service)]
):
    employee = await employee_service.soft_delete(employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"status": "success", "message": f"Employee {employee_id} soft-deleted"}