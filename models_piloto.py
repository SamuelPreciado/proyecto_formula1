from sqlmodel import SQLModel, Field
from typing import Optional

class Piloto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    escuderia: str
    nacionalidad: str
    puntos: int
    activo: bool = Field(default=True)
    imagen: Optional[str] = Field(default=None, description="Nombre del archivo de imagen del piloto")