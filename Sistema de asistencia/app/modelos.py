from pydantic import BaseModel, Field, EmailStr # Validación de datos y correos

# 1. Clase de Asistente (Reglas para los datos del alumno)
class asistente(BaseModel):
    id: int = Field(..., gt=0, description="identificador obligatorio mayor a cero")
    nombre: str = Field(..., min_length=3, max_length=50)
    correo: EmailStr = Field(..., description="correo electrónico válido")

# 2. Clase de Conferencia (Reglas para las pláticas del evento)
class conferencia(BaseModel):
    id_conf: int = Field(..., gt=0)
    tema: str = Field(..., min_length=5, max_length=100)
    ponente: str = Field(..., min_length=3)
    cupo_maximo: int = Field(..., ge=10, le=100)
