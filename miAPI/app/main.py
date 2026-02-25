from fastapi import FastAPI, status, HTTPException
import asyncio
from typing import Optional
from pydantic import BaseModel, Field

app = FastAPI(
    title = "Mi Primera API",
    description = "Andrés Joshua León Barranco",
    version = "1.0"
)

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

usuarios = [
    {"id":1, "nombre":"Jorge", "edad":"20"},
    {"id":2, "nombre":"Beto Normal", "edad":"20"},
    {"id":3, "nombre":"Cris", "edad":"22"},
    {"id":4, "nombre":"Lalo", "edad":"20"}
]

class crear_usuario(BaseModel):
    id: int = Field(..., gt = 0, description = "Identificador de usuario")
    nombre: str = Field(..., min_length = 3, max_length = 50, example = "John Doe")
    edad: int = Field(..., min_length = 1, max_length = 125, description = "Edad válida entre 1 y 125")

@app.get("/v1/ParametroOb/{id}", tags = ['Parametro obligatorio'])
async def consultauno(id:int):
    return {"Mensaje": "Usuario encontrado",
            "Usuario": id,
            "Status": "200"
            }

@app.get("/v1/ParametroOp/", tags = ['Parametro opcional'])
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

@app.get("/v1/usuarios/", tags = ['CRUD HTTP'])
async def consultaT():
    return{
        "status": "200",
        "total": len(usuarios),
        "Usuarios": usuarios
    }

@app.post("/v1/usuarios/", tags = ['CRUD HTTP'])
async def agregar_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code = 400,
                detail = "El id ya existe."
            )
    usuarios.append(usuario)
    return {
        "Mensaje" : "Usuario agregado",
        "Usuario" : usuario,
        "Status" : "200"
    }

@app.put("/v1/usuarios/{id}", tags = ['CRUD HTTP'])
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index].update(usuario_actualizado)
            return {
                "Mensaje": "Usuario actualizado",
                "Usuario": usuarios[index],
                "Status": "200"
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags = ['CRUD HTTP'])
async def eliminar_usuario(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "Mensaje": "Usuario eliminado",
                "Status": "200"
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


# Con este comando se ejecuta el servidor y le asignamos un puerto: 
# uvicorn main:app --reload --port 5000