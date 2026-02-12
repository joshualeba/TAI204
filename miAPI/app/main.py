# Importaciones
from fastapi import FastAPI
import asyncio
from typing import Optional

# Instancia del servidor
app = FastAPI(
    title = "Mi Primera API",
    description = "Andrés Joshua León Barranco",
    version = "1.0"
)

# Endpoints
@app.get("/", tags = ['Inicio'])
async def bienvenido():
    return {"Mensaje": "Bienvenido a FastAPI"}

@app.get("/holaMundo", tags = ['Asincronia'])
async def Hola():
    await asyncio.sleep(5)
    return {
        "Mensaje": "Hola Mundo FastAPI",
        "Status": "200"
    }

#TB ficticia
usuarios = [
    {"id":1, "nombre":"Diego", "edad":"21"},
    {"id":2, "nombre":"Cristiano", "edad":"21"},
    {"id":3, "nombre":"Betito", "edad":"21"},
]

@app.get("/v1/usuario/{id}", tags = ['Parametro obligatorio'])
async def consultauno(id:int):
    return {"Mensaje": "Usuario encontrado",
            "Usuario": id,
            "Status": "200"
            }

@app.get("/v1/usuarios/", tags = ['Parametro opcional'])
async def consultatodos(id:Optional[int] = None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return{"Mensaje": "Usuario encontrado",
                       "Usuario": usuarioK,
                       "Status": "200"
                       }
        return{"Mensaje": "Usuario no encontrado",
               "Status": "200"
               }
    else:
        return {"Mensaje":"No se proporcionó ID"}
    
