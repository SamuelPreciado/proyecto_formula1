from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.ext.declarative import declarative_base
import contextlib
from sqlmodel import SQLModel

CLEVER_DB = (
    "postgresql+asyncpg://uxvzn3b7cgwi95jff61f:HH11sQzeFmenVZ5fMdOgT5blLISQwu@"
    "bsgpdihy3vwaex0141iw-postgresql.services.clever-cloud.com:"
    "50013/bsgpdihy3vwaex0141iw"
)


engine = create_async_engine(CLEVER_DB,echo=False,
    pool_size=3,
    max_overflow=0,
    pool_timeout=30,
    pool_pre_ping=True,
    pool_recycle=60,
    poolclass=AsyncAdaptedQueuePool
)





async_session_maker = async_sessionmaker(engine,class_=AsyncSession,expire_on_commit=False,autocommit=False,
    autoflush=False

)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db_connections():
    await engine.dispose()


@contextlib.asynccontextmanager
async def get_session():
    session = async_session_maker()
    try:
        yield session
    except Exception as e:
        await session.rollback()
        raise e
    finally:
        await session.close()


