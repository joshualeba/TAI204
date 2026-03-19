from pydantic import BaseModel, Field

# Reglas para crear o validar un usuario
class crear_usuario(BaseModel):
    id: int = Field(..., gt = 0, description = "Identificador de usuario") # ID mayor a 0
    nombre: str = Field(..., min_length = 3, max_length = 50, example = "John Doe") # Nombre real
    edad: int = Field(..., min_length = 1, max_length = 125, description = "Edad válida entre 1 y 125")