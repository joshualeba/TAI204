from fastapi import status, HTTPException, Depends, APIRouter
from app.data.database import usuarios
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

router = APIRouter(
    prefix = "/v1/usuarios",
    tags = ['CRUD HTTP']
)

# --- Sección GET ---
@router.get("/")
async def consulta_total():
    return{
        "status": "200",
        "total": len(usuarios),
        "usuarios": usuarios
    }

# --- Sección POST ---
@router.post("/")
async def agregar_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(
                status_code = 400,
                detail = "El id ya existe."
            )
    usuarios.append(usuario)
    return {
        "mensaje" : "Usuario agregado",
        "usuario" : usuario,
        "status" : "200"
    }

# --- Sección PUT ---
@router.put("/{id}")
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index].update(usuario_actualizado)
            return {
                "mensaje": "Usuario actualizado",
                "usuario": usuarios[index],
                "status": "200"
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# --- Sección PATCH ---
@router.patch("/{id}")
async def actualizacion_parcial_usuario(id: int, campos_a_modificar: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index].update(campos_a_modificar)
            return {
                "mensaje": "Usuario actualizado parcialmente",
                "usuario": usuarios[index],
                "status": "200"
            }
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# --- Sección DELETE ---
@router.delete("/")
async def eliminar_usuario(id: int, usuario_auth:str = Depends(verificar_peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": f"Usuario eliminado por {usuario_auth}",
                "status": "200"
            }
    raise HTTPException(status_code = 404, detail="Usuario no encontrado")