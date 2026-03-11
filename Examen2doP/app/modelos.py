from pydantic import BaseModel, Field

class clientes(BaseModel):
    id: int = Field(..., gt=0, description="identificador obligatorio mayor a cero")
    nombre: str = Field(..., min_length = 8, max_length=50)

class turnos(BaseModel):
    id_tur: int = Field(..., gt=0)
    tema: str = Field(..., min_length=5, max_length=100)
    fecha: int = Field(..., ge=10, le=100)

class tramite(BaseModel):
    id_tra: int = Field(..., gt = 0)
    tipo_tra: str = Field(..., min_length = 5, max_length = 20)

