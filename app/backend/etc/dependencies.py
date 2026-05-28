from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.backend.db.database import get_db
from app.backend.schemas.contexts import RequestContext


def get_context(request: Request) -> RequestContext:
    ctx = getattr(request.state, "context", None)
    if ctx is None:
        raise RuntimeError("RequestContext not found. Is middleware enabled?")
    return ctx


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db():
        yield session
