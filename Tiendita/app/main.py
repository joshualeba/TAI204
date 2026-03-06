from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title = "API tiendita",
    description = "Andrés Joshua León Barranco",
    version = "1.0"
)

class producto(BaseModel):
    id: int = Field(..., gt = 0)
    nombre: str = Field(..., min_length = 3, max_length = 50)
    precio: float = Field(..., ge = 1, le = 100000)
    cantidad: int = Field(..., ge = 1, le = 1000)

inventario = []

@app.get("/productos")
def obtener_productos():
    return inventario

@app.post("/productos")
def crear_producto(producto: producto):
    inventario.append(producto)
    return {"mensaje": "producto agregado exitosamente"}
