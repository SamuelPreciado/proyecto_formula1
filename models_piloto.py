
from pydantic import BaseModel # type: ignore

class Piloto(BaseModel):
    id: int
    nombre: str
    escuderia: str
    nacionalidad: str
    puntos: int
    activo: bool = True
