from typing import AsyncGenerator
from app.database.database import engine
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db_session_with_commit() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSession(engine)
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()