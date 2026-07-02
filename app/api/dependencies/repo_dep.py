from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from contracts import EmployeesRepositoryProtocol
from repositories import EmployeesRepository
from .db_session_dep import get_db_session_with_commit


async def get_employee_repository(
    session: AsyncSession = Depends(get_db_session_with_commit)
) -> EmployeesRepositoryProtocol:
    return EmployeesRepository(session)
