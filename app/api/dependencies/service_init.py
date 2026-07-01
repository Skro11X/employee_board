from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends 
from app.api.dependencies.db_session_dep import get_db_session_with_commit


async def some_service(session: AsyncSession = Depends(get_db_session_with_commit)):
    pass
    
    # return SomeService(semd_repo, file_repo, storage)