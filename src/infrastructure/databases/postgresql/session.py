from .session_manager import sessionmanager
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncIterator

async def get_session() -> AsyncIterator[AsyncSession]:
    async with sessionmanager.session() as session:
        yield session
