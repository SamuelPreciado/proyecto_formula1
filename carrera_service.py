from typing import List, Optional
from sqlmodel import select
from models_carrera import Carrera
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from database_connection import get_session

async def get_all_carreras(session: AsyncSession = Depends(get_session)) -> List[Carrera]:
    result = await session.execute(select(Carrera).where(Carrera.activo == True))
    return result.scalars().all()

async def get_carrera_by_id(carrera_id: int, session: AsyncSession = Depends(get_session)) -> Optional[Carrera]:
    return await session.get(Carrera, carrera_id)

async def create_carrera(carrera: Carrera, session: AsyncSession = Depends(get_session)):
    existing = await session.get(Carrera, carrera.id)
    if existing:
        raise ValueError(f"Ya existe una carrera con ID {carrera.id}")
    session.add(carrera)
    try:
        await session.commit()
    except SQLAlchemyError as e:
        await session.rollback()
        raise RuntimeError(f"Error al crear carrera: {e}")

async def update_carrera(carrera_id: int, updated: Carrera, session: AsyncSession) -> Carrera:
    try:
        stmt = select(Carrera).where(Carrera.id == carrera_id)
        result = await session.execute(stmt)
        db_carrera = result.scalar_one_or_none()

        if not db_carrera:
            raise HTTPException(status_code=404, detail=f"Carrera con ID {carrera_id} no encontrado")

        # Actualizar solo los campos no nulos
        update_data = updated.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_carrera, key, value)

        await session.commit()  # <-- ESTO FALTABA
        await session.refresh(db_carrera)
        return db_carrera
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar carrera: {str(e)}")

async def delete_carrera(carrera_id: int, session: AsyncSession = Depends(get_session)):
    carrera = await session.get(Carrera, carrera_id)
    if carrera:
        carrera.activo = False
        session.add(carrera)
        await session.commit()

async def filter_carreras_por_pais(pais: str, session: AsyncSession = Depends(get_session)) -> List[Carrera]:
    result = await session.execute(
        select(Carrera).where(Carrera.activo == True, Carrera.pais.ilike(f"%{pais}%"))
    )
    return result.scalars().all()

async def buscar_carrera_por_ganador(ganador: str, session: AsyncSession = Depends(get_session)) -> List[Carrera]:
    result = await session.execute(
        select(Carrera).where(Carrera.activo == True, Carrera.ganador.ilike(f"%{ganador}%"))
    )
    return result.scalars().all()

async def get_carreras_borradas(session: AsyncSession = Depends(get_session)) -> List[Carrera]:
    result = await session.execute(select(Carrera).where(Carrera.activo == False))
    return result.scalars().all()
