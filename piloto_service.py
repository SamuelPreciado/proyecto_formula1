

from typing import List, Optional
from models_piloto import Piloto
from utils import read_csv, write_csv
from utils import ensure_csv_exists
FILEPATH = "data/pilotos.csv"

def _load_pilotos() -> List[Piloto]:
    try:
        ensure_csv_exists(FILEPATH, ["id", "nombre", "escuderia", "nacionalidad", "puntos", "activo"])
        raw = read_csv(FILEPATH)
        return [Piloto(**{
            **item,
            "id": int(item["id"]),
            "puntos": int(item["puntos"]),
            "activo": item["activo"] == "True"
        }) for item in raw]
    except (KeyError, ValueError) as e:
        raise RuntimeError(f"Error al cargar pilotos desde el CSV: {e}")
    except Exception as e:
        raise RuntimeError(f"Error inesperado al leer pilotos: {e}")

def _save_pilotos(pilotos: List[Piloto]):
    data = [p.dict() for p in pilotos]
    write_csv(FILEPATH, data)

def get_all_pilotos() -> List[Piloto]:
    return [p for p in _load_pilotos() if p.activo]

def get_piloto_by_id(piloto_id: int) -> Optional[Piloto]:
    for piloto in _load_pilotos():
        if piloto.id == piloto_id:
            return piloto
    return None

def create_piloto(piloto: Piloto):
    pilotos = _load_pilotos()
    if any(p.id == piloto.id for p in pilotos):
        raise ValueError(f"Ya existe un piloto con ID {piloto.id}")
    pilotos.append(piloto)
    _save_pilotos(pilotos)

def update_piloto(piloto_id: int, updated: Piloto):
    pilotos = _load_pilotos()
    found = False
    for i, p in enumerate(pilotos):
        if p.id == piloto_id:
            pilotos[i] = updated
            found = True
            break
    if not found:
        raise ValueError(f"No se encontró piloto con ID {piloto_id}")
    _save_pilotos(pilotos)

def delete_piloto(piloto_id: int):
    pilotos = _load_pilotos()
    for piloto in pilotos:
        if piloto.id == piloto_id:
            piloto.activo = False
            break
    _save_pilotos(pilotos)

def filter_pilotos_by_escuderia(escuderia: str) -> List[Piloto]:
    return [p for p in _load_pilotos() if p.activo and escuderia.lower() in p.escuderia.lower()]

def search_piloto_by_nombre(nombre: str) -> List[Piloto]:
    return [p for p in _load_pilotos() if p.activo and nombre.lower() in p.nombre.lower()]

def get_pilotos_borrados() -> List[Piloto]:
    return [p for p in _load_pilotos() if not p.activo]



