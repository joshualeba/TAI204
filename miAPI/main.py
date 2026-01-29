# Importaciones
from fastapi import FastAPI
import asyncio

# Instancia del servidor
app = FastAPI()

# Endpoints
@app.get("/")
async def bienvenido():
    return {"Mensaje": "Bienvenido a FastAPI"}

@app.get("/holaMundo")
async def Hola():
    await asyncio.sleep(5)
    return {
        "Mensaje": "Hola Mundo FastAPI",
        "Status": "200"
    }