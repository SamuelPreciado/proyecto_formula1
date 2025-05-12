from sqlalchemy.ext.asyncio import create_async_engine, async_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel

CLEVER_DB = (
    "postgresql+asyncpg://uxvzn3b7cgwi95jff61f:HH11sQzeFmenVZ5fMdOgT5blLISQwu@"
    "bsgpdihy3vwaex0141iw-postgresql.services.clever-cloud.com:"
    "50013/uxvzn3b7cgwi95jff61f"
)

engine = create_async_engine(CLEVER_DB, echo=True, future=True)

asyncsession = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session():
    async with async_session() as session:
        yield session