from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from app.data.db import get_db
from app.data.usuario import Usuario as usuarioDB
from app.models.usuarios import crear_usuario
from app.security.auth import verificar_peticion

router = APIRouter(
    prefix="/v1/usuarios",
    tags=['CRUD HTTP']
)

# --- Sección GET ---
@router.get("/")
async def leer_usuarios(db: Session = Depends(get_db)):
    usuarios_db = db.query(usuarioDB).all()
    return {
        "status": "200",
        "total": len(usuarios_db),
        "usuarios": usuarios_db
    }

# --- Sección POST ---
@router.post("/", status_code=status.HTTP_201_CREATED)
async def registrar_usuario(usuarioP: crear_usuario, db: Session = Depends(get_db)):
    # 1. Creamos la instancia del modelo con los datos que llegan
    usuarioNuevo = usuarioDB(nombre=usuarioP.nombre, edad=usuarioP.edad)
    
    # 2. Preparamos y guardamos en la base de datos
    db.add(usuarioNuevo)
    db.commit()
    db.refresh(usuarioNuevo)
    
    return {
        "mensaje": "Usuario agregado",
        "usuario": usuarioNuevo,
        "status": "201"
    }

# --- Sección PUT ---
@router.put("/{id}")
async def actualizar_usuario(id: int, usuarioP: crear_usuario, db: Session = Depends(get_db)):
    usuario_en_db = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    
    if not usuario_en_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizamos los campos manualmente
    usuario_en_db.nombre = usuarioP.nombre
    usuario_en_db.edad = usuarioP.edad
    
    db.commit()
    db.refresh(usuario_en_db)
    return {
        "mensaje": "Usuario actualizado",
        "usuario": usuario_en_db,
        "status": "200"
    }

# --- Sección DELETE ---
@router.delete("/{id}")
async def eliminar_usuario(id: int, db: Session = Depends(get_db), usuario_auth: str = Depends(verificar_peticion)):
    usuario_en_db = db.query(usuarioDB).filter(usuarioDB.id == id).first()
    
    if not usuario_en_db:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    db.delete(usuario_en_db)
    db.commit()
    return {
        "mensaje": f"Usuario eliminado por {usuario_auth}",
        "status": "200"
    }