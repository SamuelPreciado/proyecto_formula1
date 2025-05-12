from pydantic import BaseModel
from typing import List
from models_piloto import Piloto
from models_carrera import Carrera

class RespuestaBorrados(BaseModel):
    pilotos_eliminados: List[Piloto]
    carreras_eliminadas: List[Carrera]
