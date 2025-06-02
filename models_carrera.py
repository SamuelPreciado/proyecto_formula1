from sqlmodel import SQLModel, Field
from typing import Optional

class Carrera(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    pais: str
    fecha: str
    ganador: str
    vueltas: int
    activo: bool = True
