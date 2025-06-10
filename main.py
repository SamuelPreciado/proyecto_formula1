from fastapi import FastAPI, HTTPException, Depends, Request, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List
import piloto_service
import carrera_service
from models_piloto import Piloto
from models_carrera import Carrera
from models_respuesta import RespuestaBorrados
from database_connection import get_session, engine, init_db
import os
import shutil
app = FastAPI()

# Eventos
@app.on_event("startup")
async def on_startup():
    await init_db()

@app.on_event("shutdown")
async def shutdown():
    await engine.dispose()

# Configurar archivos estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



@app.get("/")
@app.get("/index.html")
async def read_root(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request, "titulo": "¡Bienvenido a mi Proyecto FastAPI!"},
    )

@app.get("/diseño.html")
@app.get("/diseño.html")
async def get_diseno(request: Request):
    return templates.TemplateResponse(
        name="diseño.html",
        context={"request": request, "titulo": "Diseño Del proyecto"},
    )
@app.get("/planeacion.html")
@app.get("/planeacion.html")
async def get_planeacion(request: Request):
    return templates.TemplateResponse(
        name="planeacion.html",
        context={"request": request, "titulo": "Planeacion Del proyecto"},
    )
@app.get("/pilotos.html")
@app.get("/pilotos.html.html")
async def get_pilotos(request: Request):
    return templates.TemplateResponse(
        name="pilotos.html",
        context={"request": request, "titulo": "Pilotos del proyecto"},
    )
@app.get("/carreras.html")
@app.get("/carreras.html")
async def get_carreras(request: Request):
    return templates.TemplateResponse(
        name="carreras.html",
        context={"request": request, "titulo": "Carreras Del proyecto"},
    )
@app.get("/crear_piloto.html")
@app.get("/crear_piloto.html")
async def get_crear_piloto(request: Request):
    return templates.TemplateResponse(
        name="crear_piloto.html",
        context={"request": request, "titulo": "Crear piloto"},
    )
@app.get("/crear_piloto_imagen.html")
@app.get("/crear_piloto_imagen.html")
async def get_crear_piloto_imagen(request: Request):
    return templates.TemplateResponse(
        name="crear_piloto_imagen.html",
        context={"request": request, "titulo": "Crear piloto con imagen"},
    )
@app.get("/listar_piloto.html")
@app.get("/listar_piloto.html")
async def get_crear_piloto(request: Request):
    return templates.TemplateResponse(
        name="listar_piloto.html",
        context={"request": request, "titulo": "Listar piloto"},
    )
@app.get("/obtener_piloto.html")
@app.get("/obtener_piloto.html")
async def get_obtener_piloto(request: Request):
    return templates.TemplateResponse(
        name="obtener_piloto.html",
        context={"request": request, "titulo": "obtener piloto"},
    )
@app.get("/actualizar_piloto.html")
@app.get("/actualizar_piloto.html")
async def get_actualizar_piloto(request: Request):
    return templates.TemplateResponse(
        name="actualizar_piloto.html",
        context={"request": request, "titulo": "Actualizar piloto"},
    )
@app.get("/filtrar_escuderia.html")
@app.get("/filtrar_escuderia.html.html")
async def get_filtrar_escuderia(request: Request):
    return templates.TemplateResponse(
        name="filtrar_escuderia.html",
        context={"request": request, "titulo": "Filtrar por escuderia"},
    )
@app.get("/buscar_piloto.html")
@app.get("/buscar_piloto.html")
async def get_buscar_piloto(request: Request):
    return templates.TemplateResponse(
        name="buscar_piloto.html",
        context={"request": request, "titulo": "Buscar piloto"},
    )
@app.get("/eliminar_piloto.html")
@app.get("/eliminar_piloto.html")
async def get_eliminar_piloto(request: Request):
    return templates.TemplateResponse(
        name="eliminar_piloto.html",
        context={"request": request, "titulo": "Eliminar piloto"},
    )
@app.get("/crear_carrera_imagen.html")
@app.get("/crear_carrera_imagen.html")
async def get_crear_carrera_imagen(request: Request):
    return templates.TemplateResponse(
        name="crear_carrera_imagen.html",
        context={"request": request, "titulo": "Crear carrera con imagen"},
    )
@app.get("/crear_carrera.html")
@app.get("/crear_carrera.html")
async def get_crear_carrera(request: Request):
    return templates.TemplateResponse(
        name="crear_carrera.html",
        context={"request": request, "titulo": "Crear carrera"},
    )
@app.get("/listar_carrera.html")
@app.get("/listar_carrera.html")
async def get_listar_carrera(request: Request):
    return templates.TemplateResponse(
        name="listar_carrera.html",
        context={"request": request, "titulo": "Listar carrera"},
    )
@app.get("/obtener_carrera.html")
@app.get("/obtener_carrera.html")
async def get_obtener_carrera(request: Request):
    return templates.TemplateResponse(
        name="obtener_carrera.html",
        context={"request": request, "titulo": "Obtener carrera"},
    )
@app.get("/actualizar_carrera.html")
@app.get("/actualizar_carrera.html")
async def get_actualizar_carrera(request: Request):
    return templates.TemplateResponse(
        name="actualizar_carrera.html",
        context={"request": request, "titulo": "Actualizar carrera"},
    )
@app.get("/filtrar_pais.html")
@app.get("/filtrar_pais.html")
async def get_filtrar_pais(request: Request):
    return templates.TemplateResponse(
        name="filtrar_pais.html",
        context={"request": request, "titulo": "Filtrar por pais"},
    )
@app.get("/buscar_carrera.html")
@app.get("/buscar_carrera.html")
async def get_buscar_carrera(request: Request):
    return templates.TemplateResponse(
        name="buscar_carrera.html",
        context={"request": request, "titulo": "Buscar carrera"},
    )
@app.get("/eliminar_carrera.html")
@app.get("/eliminar_carrera.html")
async def get_eliminar_carrera(request: Request):
    return templates.TemplateResponse(
        name="eliminar_carrera.html",
        context={"request": request, "titulo": "Eliminar carrera"},
    )
@app.get("/obtener_pilotos_borrados.html")
@app.get("/obtener_pilotos_borrados.html")
async def get_obtener_pilotos_borrados(request: Request):
    return templates.TemplateResponse(
        name="obtener_pilotos_borrados.html",
        context={"request": request, "titulo": "Obtener pilotos borrados"},
    )
@app.get("/obtener_carreras_borradas.html")
@app.get("/obtener_carreras_borradas.html")
async def get_obtener_carreras_borradas(request: Request):
    return templates.TemplateResponse(
        name="obtener_carreras_borradas.html",
        context={"request": request, "titulo": "Obtener carreras borradas"},
    )

# ------------------ PILOTOS ------------------
@app.get("/pilotos", response_model=List[Piloto])
async def listar_pilotos(session: AsyncSession = Depends(get_session)):
    return await piloto_service.get_all_pilotos(session)

@app.get("/pilotos/{piloto_id}", response_model=Piloto)
async def obtener_piloto(piloto_id: int, session: AsyncSession = Depends(get_session)):
    piloto = await piloto_service.get_piloto_by_id(piloto_id, session)
    if not piloto or not piloto.activo:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    return piloto


@app.post("/pilotos/crear_con_imagen", status_code=201)
async def crear_piloto_con_imagen(
        id: int = Form(...),
        nombre: str = Form(...),
        escuderia: str = Form(...),
        nacionalidad: str = Form(...),
        puntos: int = Form(...),
        activo: bool = Form(...),
        imagen: UploadFile = File(...),
        session: AsyncSession = Depends(get_session)
):
    import os
    import shutil

    uploads_dir = "static/uploads"
    os.makedirs(uploads_dir, exist_ok=True)
    imagen_filename = imagen.filename  # <-- ESTE ES EL PARÁMETRO
    imagen_path = os.path.join(uploads_dir, imagen_filename)
    with open(imagen_path, "wb") as buffer:
        shutil.copyfileobj(imagen.file, buffer)

    piloto_data = Piloto(
        id=id,
        nombre=nombre,
        escuderia=escuderia,
        nacionalidad=nacionalidad,
        puntos=puntos,
        activo=activo,
        imagen=imagen_filename
    )
    await piloto_service.create_piloto(piloto_data, session)
    return {"mensaje": "Piloto creado exitosamente con imagen"}
@app.post("/pilotos", status_code=201)
async def crear_piloto(piloto: Piloto, session: AsyncSession = Depends(get_session)):
    await piloto_service.create_piloto(piloto, session)
    return {"mensaje": "Piloto creado exitosamente"}


@app.put("/pilotos/{piloto_id}")
async def actualizar_piloto(piloto_id: int, piloto: Piloto, session: AsyncSession = Depends(get_session)):
    await piloto_service.update_piloto(piloto_id, piloto, session)
    return {"mensaje": "Piloto actualizado correctamente"}

@app.delete("/pilotos/{piloto_id}")
async def eliminar_piloto(piloto_id: int, session: AsyncSession = Depends(get_session)):
    piloto = await piloto_service.get_piloto_by_id(piloto_id, session)
    if not piloto or not piloto.activo:
        raise HTTPException(status_code=404, detail="Piloto no encontrado")
    await piloto_service.delete_piloto(piloto_id, session)
    return {"mensaje": "Piloto eliminado (lógicamente)"}

@app.get("/pilotos/escuderia/{escuderia}", response_model=List[Piloto])
async def filtrar_por_escuderia(escuderia: str, session: AsyncSession = Depends(get_session)):
    return await piloto_service.filter_pilotos_by_escuderia(escuderia, session)

@app.get("/pilotos/buscar/{nombre}", response_model=List[Piloto])
async def buscar_por_nombre(nombre: str, session: AsyncSession = Depends(get_session)):
    return await piloto_service.search_piloto_by_nombre(nombre, session)

# ------------------ CARRERAS ------------------
@app.get("/carreras", response_model=List[Carrera])
async def listar_carreras(session: AsyncSession = Depends(get_session)):
    return await carrera_service.get_all_carreras(session)

@app.get("/carreras/{carrera_id}", response_model=Carrera)
async def obtener_carrera(carrera_id: int, session: AsyncSession = Depends(get_session)):
    carrera = await carrera_service.get_carrera_by_id(carrera_id, session)
    if not carrera or not carrera.activo:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return carrera

@app.post("/carreras/crear_con_imagen", status_code=201)
async def crear_carrera_con_imagen(
    id: int = Form(...),
    nombre: str = Form(...),
    pais: str = Form(...),
    fecha: str = Form(...),
    vueltas: int = Form(...),
    ganador: str = Form(...),
    activo: bool = Form(...),
    imagen: UploadFile = File(...),
    session: AsyncSession = Depends(get_session)
):
    upload_dir = "static/uploads"
    os.makedirs(upload_dir, exist_ok=True)
    imagen_filename = imagen.filename
    imagen_path = os.path.join(upload_dir, imagen_filename)
    with open(imagen_path, "wb") as buffer:
        shutil.copyfileobj(imagen.file, buffer)

    carrera_data = Carrera(
        id=id,
        nombre=nombre,
        pais=pais,
        fecha=fecha,
        vueltas=vueltas,
        ganador=ganador,
        activo=activo,
        imagen=imagen_filename
    )
    await carrera_service.create_carrera(carrera_data, session)
    return {"mensaje": "Carrera creada exitosamente con imagen"}
@app.post("/carreras", status_code=201)
async def crear_carrera(carrera: Carrera, session: AsyncSession = Depends(get_session)):
    await carrera_service.create_carrera(carrera, session)
    return {"mensaje": "Carrera creada exitosamente"}

@app.put("/carreras/{carrera_id}")
async def actualizar_carrera(carrera_id: int, carrera: Carrera, session: AsyncSession = Depends(get_session)):
    await carrera_service.update_carrera(carrera_id, carrera, session)
    return {"mensaje": "Carrera actualizada correctamente"}

@app.delete("/carreras/{carrera_id}")
async def eliminar_carrera(carrera_id: int, session: AsyncSession = Depends(get_session)):
    carrera = await carrera_service.get_carrera_by_id(carrera_id, session)
    if not carrera or not carrera.activo:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    await carrera_service.delete_carrera(carrera_id, session)
    return {"mensaje": "Carrera eliminada (lógicamente)"}

@app.get("/carreras/pais/{pais}", response_model=List[Carrera])
async def filtrar_por_pais(pais: str, session: AsyncSession = Depends(get_session)):
    return await carrera_service.filter_carreras_por_pais(pais, session)

@app.get("/carreras/buscar/{ganador}", response_model=List[Carrera])
async def buscar_por_ganador(ganador: str, session: AsyncSession = Depends(get_session)):
    return await carrera_service.buscar_carrera_por_ganador(ganador, session)

# ------------------ BORRADOS ------------------
@app.get("/borrados", response_model=RespuestaBorrados)
async def obtener_borrados(session: AsyncSession = Depends(get_session)):
    pilotos_borrados = await piloto_service.get_pilotos_borrados(session)
    carreras_borradas = await carrera_service.get_carreras_borradas(session)
    return {
        "pilotos_eliminados": pilotos_borrados,
        "carreras_eliminadas": carreras_borradas
    }
