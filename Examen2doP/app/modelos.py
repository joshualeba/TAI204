from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class Turno(BaseModel):
    id: int = Field(..., gt=0)
    cliente: str = Field(..., min_length=8)
    tipo_tramite: str
    fecha: datetime
    atendido: bool = False

    @field_validator("tipo_tramite")
    def validar_tramite(cls, v):
        opciones = ["depósito", "retiro", "consulta"]
        if v.lower() not in opciones:
            raise ValueError("El tipo de trámite debe ser depósito, retiro o consulta")
        return v.lower()

    @field_validator("fecha")
    def validar_fecha(cls, v):
        if v <= datetime.now():
            raise ValueError("La fecha del turno debe ser futura")
        if not (9 <= v.hour < 15):
            raise ValueError("La fecha del turno debe estar entre las 9 am y las 3 pm")
        return v