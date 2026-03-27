from pydantic import BaseModel, Field

# Reglas para crear o validar un usuario
class crear_usuario(BaseModel):
    nombre: str = Field(..., min_length = 3, max_length = 50, example = "John Doe") # Nombre real
    edad: int = Field(..., ge = 1, le = 125, description = "Edad válida entre 1 y 125")

# Reglas para actualizar parcialmente un usuario (patch)
class actualizar_usuario_parcial(BaseModel):
    nombre: str | None = Field(None, min_length = 3, max_length = 50, example = "John Doe")
    edad: int | None = Field(None, ge = 1, le = 125, description = "Edad válida entre 1 y 125")