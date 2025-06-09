from typing import List, Optional, Any, Coroutine, Sequence
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select
from models_piloto import Piloto
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from database_connection import get_session

async def get_all_pilotos(session: AsyncSession) -> List[Piloto]:
    try:
        stmt = select(Piloto).where(Piloto.activo == True)
        result = await session.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener pilotos: {str(e)}")


async def get_piloto_by_id(piloto_id: int, session: AsyncSession) -> Optional[Piloto]:
    try:
        stmt = select(Piloto).where(Piloto.id == piloto_id)
        result = await session.execute(stmt)
        piloto = result.scalar_one_or_none()
        if not piloto:
            raise HTTPException(status_code=404, detail=f"Piloto con ID {piloto_id} no encontrado")
        return piloto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener piloto: {str(e)}")


async def create_piloto(piloto: Piloto, session: AsyncSession = Depends(get_session)):
    existing = await session.get(Piloto, piloto.id)
    if existing:
        raise ValueError(f"Ya existe un piloto con ID {piloto.id}")
    session.add(piloto)
    try:
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise RuntimeError(f"Error al crear piloto: {e}")


async def update_piloto(piloto_id: int, updated: Piloto, session: AsyncSession) -> Piloto:
    try:
        stmt = select(Piloto).where(Piloto.id == piloto_id)
        result = await session.execute(stmt)
        db_piloto = result.scalar_one_or_none()

        if not db_piloto:
            raise HTTPException(status_code=404, detail=f"Piloto con ID {piloto_id} no encontrado")

        # Actualizar solo los campos no nulos
        update_data = updated.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_piloto, key, value)

        await session.commit()  # <-- ESTO FALTABA
        await session.refresh(db_piloto)
        return db_piloto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar piloto: {str(e)}")



async def delete_piloto(piloto_id: int, session: AsyncSession = Depends(get_session)):
    piloto = await session.get(Piloto, piloto_id)
    if piloto:
        piloto.activo = False
        session.add(piloto)
        await session.commit()


async def filter_pilotos_by_escuderia(escuderia: str, session: AsyncSession) -> List[Piloto]:
    try:
        # Simplemente usar la sesión directamente
        stmt = select(Piloto).where(
            Piloto.escuderia.ilike(f"%{escuderia}%"),
            Piloto.activo == True
        )
        result = await session.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al filtrar por escudería: {str(e)}"
        )




async def search_piloto_by_nombre(nombre: str, session: AsyncSession) -> List[Piloto]:
    try:
        stmt = select(Piloto).where(
            Piloto.nombre.ilike(f"%{nombre}%"),
            Piloto.activo == True
        )
        result = await session.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar por nombre: {str(e)}")


async def get_pilotos_borrados(session: AsyncSession) -> List[Piloto]:
    try:
        stmt = select(Piloto).where(Piloto.activo == False)
        result = await session.execute(stmt)
        return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener pilotos borrados: {str(e)}")