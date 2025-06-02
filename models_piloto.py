
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date # type: ignore

class Piloto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    escuderia: str
    nacionalidad: str
    puntos: int
    activo: bool = True
