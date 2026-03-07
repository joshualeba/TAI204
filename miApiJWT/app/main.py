from fastapi import FastAPI, status, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta

app = FastAPI(
    title = "Mi api jwt",
    description = "Andrés joshua león barranco",
    version = "1.1"
)

SECRET_KEY = "mi_llave_secreta_super_segura"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def crear_token_acceso(datos: dict, tiempo_expiracion: Optional[timedelta] = None):
    datos_copia = datos.copy()
    if tiempo_expiracion:
        expiracion = datetime.utcnow() + tiempo_expiracion
    else:
        expiracion = datetime.utcnow() + timedelta(minutes=15)
    datos_copia.update({"exp": expiracion})
    return jwt.encode(datos_copia, SECRET_KEY, algorithm=ALGORITHM)

async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario: str = payload.get("sub")
        if usuario is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token no válido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return usuario
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token expirado o no válido",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.post("/token", tags=['Seguridad'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "Joshua" and form_data.password == "Contrasena1212":
        tiempo_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token_acceso = crear_token_acceso(
            datos={"sub": form_data.username}, tiempo_expiracion=tiempo_token
        )
        return {"access_token": token_acceso, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/", tags = ['Inicio'])
async def bienvenido():
    return {"Mensaje": "Bienvenido a FastAPI con JWT"}

usuarios = [
    {"id":1, "nombre":"Jorge", "edad":"20"},
    {"id":2, "nombre":"Beto Normal", "edad":"20"},
    {"id":3, "nombre":"Cris", "edad":"22"},
    {"id":4, "nombre":"Lalo", "edad":"20"}
]

class crear_usuario(BaseModel):
    id: int = Field(..., gt = 0)
    nombre: str = Field(..., min_length = 3, max_length = 50)
    edad: int = Field(..., min_length = 1, max_length = 125)

@app.get("/v1/ParametroOb/{id}", tags = ['Parámetro obligatorio'])
async def consultauno(id:int):
    return {"Mensaje": "Usuario encontrado", "Usuario": id, "Status": "200"}

@app.get("/v1/ParametroOp/", tags = ['Parámetro opcional'])
async def consultatodos(id:Optional[int] = None):
    if id is not None:
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return{"Mensaje": "Usuario encontrado", "Usuario": usuarioK, "Status": "200"}
        return{"Mensaje": "Usuario no encontrado", "Status": "200"}
    else:
        return {"Mensaje":"No se proporcionó ID"}

@app.get("/v1/usuarios/", tags = ['Crud http'])
async def consultaT():
    return{
        "status": "200",
        "total": len(usuarios),
        "Usuarios": usuarios
    }

@app.post("/v1/usuarios/", tags = ['Crud http'])
async def agregar_usuario(usuario: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuario.id:
            raise HTTPException(status_code = 400, detail = "El id ya existe.")
    usuarios.append(usuario)
    return {"Mensaje" : "Usuario agregado", "Usuario" : usuario, "Status" : "200"}

@app.put("/v1/usuarios/{id}", tags = ['Crud http'])
async def actualizar_usuario(id: int, usuario_actualizado: dict, token: str = Depends(obtener_usuario_actual)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index].update(usuario_actualizado)
            return {"Mensaje": "Usuario actualizado", "Usuario": usuarios[index], "Status": "200"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/v1/usuarios/{id}", tags = ['Crud http'])
async def eliminar_usuario(id: int, token: str = Depends(obtener_usuario_actual)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {"Mensaje": f"Usuario eliminado por {token}", "Status": "200"}
    raise HTTPException(status_code = 404, detail="Usuario no encontrado")