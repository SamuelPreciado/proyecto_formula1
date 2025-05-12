
from typing import List, Optional
from models_carrera import Carrera
from utils import read_csv, write_csv
from utils import ensure_csv_exists
FILEPATH = "data/carreras.csv"

def _load_carreras() -> List[Carrera]:
    try:
        ensure_csv_exists(FILEPATH, ["id", "nombre", "pais", "fecha", "ganador", "vueltas", "activo"])
        raw = read_csv(FILEPATH)
        carreras = []

        for item in raw:
            try:
                carrera = Carrera(
                    id=int(item["id"]),
                    nombre=item["nombre"],
                    pais=item["pais"],
                    fecha=item["fecha"],
                    ganador=item["ganador"],
                    vueltas=int(item["vueltas"]),
                    activo=item["activo"] == "True"
                )
                carreras.append(carrera)
            except (KeyError, ValueError, TypeError) as e:
                raise ValueError(f"Error al convertir datos de una carrera: {e}")
        return carreras

    except Exception as e:
        raise RuntimeError(f"No se pudieron cargar las carreras desde el archivo '{FILEPATH}': {e}")

def _save_carreras(carreras: List[Carrera]):
    data = [c.dict() for c in carreras]
    write_csv(FILEPATH, data)

def get_all_carreras() -> List[Carrera]:
    return [c for c in _load_carreras() if c.activo]

def get_carrera_by_id(carrera_id: int) -> Optional[Carrera]:
    for carrera in _load_carreras():
        if carrera.id == carrera_id:
            return carrera
    return None

def create_carrera(carrera: Carrera):
    carreras = _load_carreras()
    if any(c.id == carrera.id for c in carreras):
        raise ValueError(f"Ya existe una carrera con ID {carrera.id}")
    carreras.append(carrera)
    _save_carreras(carreras)

def update_carrera(carrera_id: int, updated: Carrera):
    carreras = _load_carreras()
    found = False
    for i, c in enumerate(carreras):
        if c.id == carrera_id:
            carreras[i] = updated
            found = True
            break
    if not found:
        raise ValueError(f"No se encontró carrera con ID {carrera_id}")
    _save_carreras(carreras)

def delete_carrera(carrera_id: int):
    carreras = _load_carreras()
    for carrera in carreras:
        if carrera.id == carrera_id:
            carrera.activo = False
            break
    _save_carreras(carreras)

def filter_carreras_por_pais(pais: str) -> List[Carrera]:
    return [c for c in _load_carreras() if c.activo and c.pais.lower() == pais.lower()]

def buscar_carrera_por_ganador(ganador: str) -> List[Carrera]:
    return [c for c in _load_carreras() if c.activo and ganador.lower() in c.ganador.lower()]

def get_carreras_borradas() -> List[Carrera]:
    return [c for c in _load_carreras() if not c.activo]
