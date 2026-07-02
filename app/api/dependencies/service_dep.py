from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends 
from app.api.dependencies.db_session_dep import get_db_session_with_commit
from services import EmployeesService
from contracts import EmployeesServiceProtocol
from .repo_dep import get_employee_repository


async def get_employee_service(repo=Depends(get_employee_repository)) -> EmployeesServiceProtocol:
    return EmployeesService(repo)


async def some_service(session: AsyncSession = Depends(get_db_session_with_commit)):
    pass
    
