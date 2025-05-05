from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import (
    async_engine_from_config,
    async_sessionmaker,
    AsyncSession,
)
from .settings import settings

database_config = settings.database.model_dump(
    mode="json", exclude={"username", "password", "name", "host", "port"}
)
database_config_sync = database_config.copy()
database_config_sync["url"] = database_config_sync["url"].replace(
    "postgresql://", "postgresql+psycopg2://"
)
db_engine = engine_from_config(
    database_config_sync,
    prefix="",
)
db_session_factory = sessionmaker(db_engine)


def get_db_session():
    with db_session_factory() as session:
        yield session


database_config_async = database_config.copy()
database_config_async["url"] = database_config_async["url"].replace(
    "postgresql://", "postgresql+asyncpg://"
)
async_db_engine = async_engine_from_config(database_config_async, prefix="")
async_db_session_factory = async_sessionmaker(async_db_engine)


async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_db_session_factory() as session:
        yield session


AsyncDBSessionDep = Annotated[AsyncSession, Depends(get_async_db_session)]
