from fastapi import FastAPI, status, HTTPException, Depends # Importamos las bases de FastAPI y dependencias
import asyncio # Para manejar tareas que tardan tiempo (esperas)
from typing import Optional # Para marcar que un dato puede ser opcional
from pydantic import BaseModel, Field # Para validar la estructura de nuestros usuarios
from fastapi.security import HTTPBasic, HTTPBasicCredentials # Para el inicio de sesión básico
import secrets # Para comparar contraseñas de forma segura

# Iniciamos nuestra primera API
app = FastAPI(
    title = "Mi Primera API", # Nombre del proyecto
    description = "Andrés Joshua León Barranco", # Autor
    version = "1.0" # Versión inicial
)

# Ruta base de bienvenida
@app.get("/", tags = ['Inicio'])
async def bienvenido():
    return {"Mensaje": "Bienvenido a FastAPI"}

# Ruta para probar la asincronía (espera 5 segundos antes de responder)
@app.get("/holaMundo", tags = ['Asincronia'])
async def Hola():
    await asyncio.sleep(5) # Simula un proceso pesado tardando 5 segundos
    return {
        "Mensaje": "Hola Mundo FastAPI",
        "Status": "200"
    }

# Datos de prueba guardados en memoria
usuarios = [
    {"id":1, "nombre":"Jorge", "edad":"20"},
    {"id":2, "nombre":"Beto Normal", "edad":"20"},
    {"id":3, "nombre":"Cris", "edad":"22"},
    {"id":4, "nombre":"Lalo", "edad":"20"}
]

# Reglas para crear o validar un usuario
class crear_usuario(BaseModel):
    id: int = Field(..., gt = 0, description = "Identificador de usuario") # ID mayor a 0
    nombre: str = Field(..., min_length = 3, max_length = 50, example = "John Doe") # Nombre real
    edad: int = Field(..., min_length = 1, max_length = 125, description = "Edad válida entre 1 y 125")

# Activamos el sistema de seguridad básico de HTTP
security = HTTPBasic()

# Función que revisa si el usuario y contraseña son correctos
def verificar_peticion(credenciales:HTTPBasicCredentials = Depends(security)):
    # Comparamos de forma segura lo que mandó el usuario contra lo que tenemos
    usuarioAuth = secrets.compare_digest(credenciales.username, "Joshua")
    contraAuth = secrets.compare_digest(credenciales.password, "Contraseña123!")

    # Si alguno está mal, lanzamos el error 401
    if not(usuarioAuth and contraAuth):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Credenciales no autorizadas"
        )
    return credenciales.username # Si todo bien, regresamos el nombre del usuario

# Consultar un solo usuario por ID en la ruta
@app.get("/v1/ParametroOb/{id}", tags = ['Parametro obligatorio'])
async def consultauno(id:int):
    return {"Mensaje": "Usuario encontrado",
            "Usuario": id,
            "Status": "200"
            }

# Consultar usuarios con parámetros al final de la URL
@app.get("/v1/ParametroOp/", tags = ['Parametro opcional'])
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

# Ver todos los usuarios del sistema
@app.get("/v1/usuarios/", tags = ['CRUD HTTP'])
async def consultaT():
    return{
        "status": "200",
        "total": len(usuarios),
        "Usuarios": usuarios
    }

# Agregar un usuario nuevo validando sus datos
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

# Actualizar los datos de un usuario existente
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

# Borrar un usuario. Esta ruta requiere estar autenticado (verificar_peticion)
@app.delete("/v1/usuarios/{id}", tags = ['CRUD HTTP'])
async def eliminar_usuario(id: int, usuarioAuth:str = Depends(verificar_peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "Mensaje": f"Usuario eliminado por {usuarioAuth}",
                "Status": "200"
            }
    raise HTTPException(status_code = 404, detail="Usuario no encontrado")