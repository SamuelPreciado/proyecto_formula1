from typing import List, Optional
from sqlmodel import select
from models_piloto import Piloto
from sqlalchemy.ext.asyncio import AsyncSession

async def get_all_pilotos(session: AsyncSession) -> List[Piloto]:
    result = await session.execute(select(Piloto).where(Piloto.activo == True))
    return result.scalars().all()

async def get_piloto_by_id(piloto_id: int, session: AsyncSession) -> Optional[Piloto]:
    return await session.get(Piloto, piloto_id)

async def create_piloto(piloto: Piloto, session: AsyncSession):
    session.add(piloto)
    await session.commit()
    await session.refresh(piloto)
    return piloto

async def update_piloto(piloto_id: int, updated: Piloto, session: AsyncSession):
    db_piloto = await session.get(Piloto, piloto_id)
    if not db_piloto:
        raise ValueError(f"No se encontró piloto con ID {piloto_id}")
    for key, value in updated.dict().items():
        setattr(db_piloto, key, value)
    await session.commit()
    await session.refresh(db_piloto)
    return db_piloto

async def delete_piloto(piloto_id: int, session: AsyncSession):
    db_piloto = await session.get(Piloto, piloto_id)
    if db_piloto:
        db_piloto.activo = False
        await session.commit()

async def filter_pilotos_by_escuderia(escuderia: str, session: AsyncSession) -> List[Piloto]:
    result = await session.execute(
        select(Piloto).where(Piloto.escuderia.ilike(f"%{escuderia}%"), Piloto.activo == True)
    )
    return result.scalars().all()

async def search_piloto_by_nombre(nombre: str, session: AsyncSession) -> List[Piloto]:
    result = await session.execute(
        select(Piloto).where(Piloto.nombre.ilike(f"%{nombre}%"), Piloto.activo == True)
    )
    return result.scalars().all()

async def get_pilotos_borrados(session: AsyncSession) -> List[Piloto]:
    result = await session.execute(select(Piloto).where(Piloto.activo == False))
    return result.scalars().all()
