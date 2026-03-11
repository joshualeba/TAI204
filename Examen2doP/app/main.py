from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import List
from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.modelos import Turno

SECRET_KEY = "llave_de_sistema"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(
    title="Api de gestión de turnos bancarios",
    version="1.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

turnos_db: List[Turno] = []

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
            raise HTTPException(status_code=401, detail="Token sin usuario")
        return usuario
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión expirada o token no válido",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username == "banco" and form_data.password == "2468":
        token = crear_token({"sub": form_data.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")

@app.get("/v1/turnos", response_model=List[Turno])
async def listar_turnos():
    return turnos_db

@app.get("/v1/turnos/{id}", response_model=Turno)
async def consultar_turno(id: int):
    turno = next((t for t in turnos_db if t.id == id), None)
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    return turno

@app.post("/v1/turnos", status_code=status.HTTP_201_CREATED)
async def crear_turno(nuevo_turno: Turno):
    if any(t.id == nuevo_turno.id for t in turnos_db):
        raise HTTPException(status_code=400, detail="El id del turno ya existe")

    fecha_dia = nuevo_turno.fecha.date()
    turnos_cliente_hoy = [
        t for t in turnos_db 
        if t.cliente == nuevo_turno.cliente and t.fecha.date() == fecha_dia
    ]
    
    if len(turnos_cliente_hoy) >= 5:
        raise HTTPException(
            status_code=400, 
            detail="No se permiten más de 5 turnos por día para el mismo cliente"
        )
    
    turnos_db.append(nuevo_turno)
    return {"mensaje": "Turno creado exitosamente", "turno": nuevo_turno}

@app.put("/v1/turnos/{id}/atendido")
async def marcar_atendido(id: int, usuario: str = Depends(validar_token)):
    turno = next((t for t in turnos_db if t.id == id), None)
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    turno.atendido = True
    return {"mensaje": f"Turno marcado como atendido por {usuario}", "turno": turno}

@app.delete("/v1/turnos/{id}")
async def eliminar_turno(id: int):
    global turnos_db
    turno = next((t for t in turnos_db if t.id == id), None)
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")
    
    turnos_db = [t for t in turnos_db if t.id != id]
    return {"mensaje": "Turno eliminado exitosamente"}
