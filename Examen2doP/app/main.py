from fastapi import FastAPI, HTTPException, Depends, status # Herramientas base de fastapi
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # Seguridad oauth2
from typing import List, Optional # Para listas y datos que pueden ser nulos
from datetime import datetime, timedelta # Manejo de fechas y expiración
from jose import jwt, JWTError # Generación y validación de tokens jwt

# IMPORTAMOS las clases desde nuestro otro archivo (modelos.py)
from app.modelos import clientes, turnos

# 1. Configuración de seguridad inicial
SECRET_KEY = "llave_de_sistema" # Llave maestra de la api
ALGORITHM = "HS256" # Algoritmo de firma
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Tiempo de vida del token (estándar de 30 min)

app = FastAPI(
    title="API de sistema de turnos bancarios",
    description="Andrés Joshua León Barranco",
    version="2.0"
)

# Esquema de seguridad: indica que el token se obtiene en /token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# "bases de datos" simuladas
clientes = []
turnos = []

# 2. Lógica de seguridad jwt profesional
def crear_token(datos: dict):
    datos_copia = datos.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos_copia.update({"exp": expiracion})
    return jwt.encode(datos_copia, SECRET_KEY, algorithm=ALGORITHM)

async def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario: str = payload.get("sub")
        if usuario is None:
            raise HTTPException(status_code=401, detail="token sin usuario")
        return usuario
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="sesión expirada o token no válido",
            headers={"WWW-Authenticate": "Bearer"},
        )

# 3. Endpoints (rutas) de la api

# Ruta para inicio de sesión
@app.post("/token", tags=['Seguridad'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "banco" and form_data.password == "2468":
        token = crear_token({"sub": form_data.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="usuario o contraseña incorrectos")

@app.get("/v1/clientes", tags=['Asistentes'])
async def listar_asistentes():
    return clientes

@app.post("/v2/asistentes", tags=['Asistentes'])
async def registrar_asistente(nuevo: asistente):
    asistentes_db.append(nuevo.model_dump())
    return {"mensaje": "asistente registrado", "datos": nuevo}

@app.get("/v1/turnos", tags=['Gestión de turnos'])
async def listar_conferencias():
    return turnos

@app.post("/v1/turnos", tags=['Gestión de turnos'])
async def crear_conferencia(nueva: turnos, usuario: str = Depends(validar_token)):
    turno.append(nueva.model_dump())
    return {"mensaje": f"conferencia creada por {usuario}", "datos": nueva}

@app.delete("/v1/{id}", tags=['Gestión de turnos'])
async def eliminar_turno(id_conf: int, usuario: str = Depends(validar_token)):
    for c in turnos:
        if c["id_conf"] == id_conf:
            turnos.remove(c)
            return {"mensaje": f"Turno eliminado por {usuario}"}
    raise HTTPException(status_code=404, detail="Turno no encontrado")












Construir una API para gestionar los turnos bancarios que permita:
