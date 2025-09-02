from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine
)
import typing as t

from .config import settings


# engine initialization
_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker[AsyncSession] | None = None


@asynccontextmanager
async def lifespan_engine(_app: FastAPI) -> t.AsyncGenerator[None, None]:
    global _engine, _sessionmaker
    if _engine is None:
        database_url = settings.database_url.unicode_string()
        _engine = create_async_engine(database_url, pool_pre_ping=True)
        _sessionmaker = async_sessionmaker(_engine, expire_on_commit=False)
    yield
    await _engine.dispose()
    _sessionmaker = None


# FastAPI recommends NOT using asynccontextmanager for yielding dependencies.
# According to the docs, FastAPI does that internally.
# @asynccontextmanager
async def lifespan_session() -> t.AsyncGenerator[AsyncSession, None]:
    assert _sessionmaker is not None, "Panic: Sessionmaker not initialized!"
    async with _sessionmaker() as session:
        try:
            yield session
            await session.commit()
        except Exception as error:
            await session.rollback()
            raise error from None
        finally:
            await session.close()

#async def get_session() -> t.AsyncGenerator[AsyncSession, None]:
#    async with lifespan_session() as session:
#        yield session

