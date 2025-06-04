from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.ext.declarative import declarative_base

from sqlmodel import SQLModel

CLEVER_DB = (
    "postgresql+asyncpg://uxvzn3b7cgwi95jff61f:HH11sQzeFmenVZ5fMdOgT5blLISQwu@"
    "bsgpdihy3vwaex0141iw-postgresql.services.clever-cloud.com:"
    "50013/bsgpdihy3vwaex0141iw"
)


engine = create_async_engine(CLEVER_DB,poolclass=AsyncAdaptedQueuePool,pool_size=5,max_overflow=10,pool_timeout=30,pool_pre_ping=True,pool_recycle=1800,
)



async_session_maker = async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False
)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()

