from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.orm import declarative_base
from typing import AsyncGenerator
from sqlmodel import SQLModel

# URL de conexión a Clever Cloud (sin espacios)
CLEVER_DB = (
    "postgresql+asyncpg://uxvzn3b7cgwi95jff61f:HH11sQzeFmenVZ5fMdOgT5blLISQwu@"
    "bsgpdihy3vwaex0141iw-postgresql.services.clever-cloud.com:50013/bsgpdihy3vwaex0141iw"
)

# Crear el engine
engine = create_async_engine(
    CLEVER_DB,
    echo=False,
    pool_size=3,
    max_overflow=0,
    pool_timeout=30,
    pool_pre_ping=True,
    pool_recycle=60,
    poolclass=AsyncAdaptedQueuePool
)

# Crear el session maker asincrónico
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Declarative base (si usas SQLAlchemy puro)
Base = declarative_base()

# Inicializar la base de datos
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

# Cerrar el engine
async def close_db_connections():
    await engine.dispose()

# Dependency para FastAPI
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
