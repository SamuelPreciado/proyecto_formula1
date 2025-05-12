from pydantic import BaseModel # type: ignore

class Carrera(BaseModel):
    id: int
    nombre: str
    pais: str
    fecha: str
    ganador: str
    vueltas: int
    activo: bool = True