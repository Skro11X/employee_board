from fastapi import Depends 
from services import EmployeesService, FileService
from contracts import EmployeesServiceProtocol
from .repo_dep import get_employee_repository


async def get_employee_service(repo=Depends(get_employee_repository)) -> EmployeesServiceProtocol:
    return EmployeesService(repo)

async def get_file_service(repo=Depends(get_employee_repository)) -> EmployeesServiceProtocol:
    return FileService()
