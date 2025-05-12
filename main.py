
from fastapi import FastAPI, HTTPException # type: ignore
from models_piloto import Piloto
import piloto_service as piloto_service
from models_carrera import Carrera
import carrera_service as carrera_service
from models_respuesta import RespuestaBorrados
from typing import List

app = FastAPI()



@app.get("/pilotos", response_model=List[Piloto])
def listar_pilotos():
    return piloto_service.get_all_pilotos()

@app.get("/pilotos/{piloto_id}", response_model=Piloto)
def obtener_piloto(piloto_id: int):
    piloto = piloto_service.get_piloto_by_id(piloto_id)
    if not piloto or not piloto.activo:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    return piloto

@app.post("/pilotos", status_code=201)
def crear_piloto(piloto: Piloto):
    try:
        piloto_service.create_piloto(piloto)
        return {"mensaje": "Piloto creado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno al crear piloto")

@app.put("/pilotos/{piloto_id}")
def actualizar_piloto(piloto_id: int, piloto: Piloto):
    try:
        piloto_service.update_piloto(piloto_id, piloto)
        return {"mensaje": "Piloto actualizado correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/pilotos/{piloto_id}")
def eliminar_piloto(piloto_id: int):
    piloto = piloto_service.get_piloto_by_id(piloto_id)
    if not piloto or not piloto.activo:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    piloto_service.delete_piloto(piloto_id)
    return {"mensaje": "Piloto eliminado (lógicamente)"}

@app.get("/pilotos/escuderia/{escuderia}", response_model=List[Piloto])
def filtrar_por_escuderia(escuderia: str):
    return piloto_service.filter_pilotos_by_escuderia(escuderia)

@app.get("/pilotos/buscar/{nombre}", response_model=List[Piloto])
def buscar_por_nombre(nombre: str):
    return piloto_service.search_piloto_by_nombre(nombre)

# 🧭 Endpoints Carreras

@app.get("/carreras", response_model=List[Carrera])
def listar_carreras():
    return carrera_service.get_all_carreras()

@app.get("/carreras/{carrera_id}", response_model=Carrera)
def obtener_carrera(carrera_id: int):
    carrera = carrera_service.get_carrera_by_id(carrera_id)
    if not carrera or not carrera.activo:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera

@app.post("/carreras", status_code=201)
def crear_carrera(carrera: Carrera):
    try:
        carrera_service.create_carrera(carrera)
        return {"mensaje": "Carrera creada exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/carreras/{carrera_id}")
def actualizar_carrera(carrera_id: int, carrera: Carrera):
    try:
        carrera_service.update_carrera(carrera_id, carrera)
        return {"mensaje": "Carrera actualizada correctamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.delete("/carreras/{carrera_id}")
def eliminar_carrera(carrera_id: int):
    carrera = carrera_service.get_carrera_by_id(carrera_id)
    if not carrera or not carrera.activo:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    carrera_service.delete_carrera(carrera_id)
    return {"mensaje": "Carrera eliminada (lógicamente)"}

@app.get("/carreras/pais/{pais}", response_model=List[Carrera])
def filtrar_por_pais(pais: str):
    return carrera_service.filter_carreras_por_pais(pais)

@app.get("/carreras/buscar/{ganador}", response_model=List[Carrera])
def buscar_por_ganador(ganador: str):
    return carrera_service.buscar_carrera_por_ganador(ganador)

@app.get("/borrados", response_model=RespuestaBorrados)
def obtener_borrados():
    pilotos_borrados = piloto_service.get_pilotos_borrados()
    carreras_borradas = carrera_service.get_carreras_borradas()
    return {
        "pilotos_eliminados": pilotos_borrados,
        "carreras_eliminadas": carreras_borradas
    }

