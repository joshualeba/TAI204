import asyncio # Para manejar tareas que tardan tiempo (esperas)
from typing import Optional # Para marcar que un dato puede ser opcional
from app.data.database import usuarios
from fastapi import APIRouter

routerV = APIRouter(
    tags = ['Inicio']
)


# Ruta base de bienvenida
@routerV.get("/")
async def bienvenido():
    return {"Mensaje": "Bienvenido a FastAPI"}

# Ruta para probar la asincronía (espera 5 segundos antes de responder)
@routerV.get("/holaMundo")
async def Hola():
    await asyncio.sleep(5) # Simula un proceso pesado tardando 5 segundos
    return {
        "Mensaje": "Hola Mundo FastAPI",
        "Status": "200"
    }

# Consultar un solo usuario por ID en la ruta
@routerV.get("/v1/ParametroOb/{id}", tags = ['Parametro obligatorio'])
async def consultauno(id:int):
    return {"Mensaje": "Usuario encontrado",
            "Usuario": id,
            "Status": "200"
            }

# Consultar usuarios con parámetros al final de la URL
@routerV.get("/v1/ParametroOp/", tags = ['Parametro opcional'])
async def consultatodos(id:Optional[int] = None):
    if id is not None:
        # Si nos dieron un id lo buscamos
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
        # Si no mandaron nada, regresamos este mensaje
        return {"Mensaje":"No se proporcionó ID"}