import datetime

from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column
from sqlalchemy import String, text

from src.config import settings

async_engine = create_async_engine(
    settings.DB_URL,
    echo=True
)
async_session = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow
)]

str_64 = Annotated[str, 64]
str_256 = Annotated[str, 256]
str_1024 = Annotated[str, 1024]


class Base(DeclarativeBase):
    type_annotation_map = {
        str_64: String(64),
        str_256: String(256),
        str_1024: String(1024),
    }
