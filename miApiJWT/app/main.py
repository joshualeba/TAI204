from fastapi import FastAPI, status, HTTPException, Depends # Importamos las herramientas básicas de FastAPI
from typing import Optional # Para manejar datos que pueden ser nulos o opcionales
from pydantic import BaseModel, Field # Para crear las reglas de nuestros objetos de datos
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm # Herramientas para el manejo de contraseñas y tokens
from jose import JWTError, jwt # Librería para crear y validar los tokens JWT
from datetime import datetime, timedelta # Para manejar fechas y tiempos de expiración

# Creamos la aplicación principal con su información básica
app = FastAPI(
    title = "Mi api jwt", # Título que se verá en la documentación
    description = "Andrés joshua león barranco", # Nombre del autor
    version = "1.1" # Versión actual del proyecto
)

# Configuraciones de seguridad necesarias para los tokens
SECRET_KEY = "mi_llave_secreta_super_segura" # Palabra clave para firmar los tokens (debe ser secreta)
ALGORITHM = "HS256" # Método matemático de encriptación
ACCESS_TOKEN_EXPIRE_MINUTES = 1 # Tiempo de vida del token (aquí es muy corto para pruebas)

# Definimos de dónde va a sacar FastAPI el token (de la ruta /token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para generar el token de acceso
def crear_token_acceso(datos: dict, tiempo_expiracion: Optional[timedelta] = None):
    datos_copia = datos.copy() # Hacemos una copia de los datos para no modificar el original
    if tiempo_expiracion:
        expiracion = datetime.utcnow() + tiempo_expiracion # Sumamos el tiempo de vida a la hora actual
    else:
        expiracion = datetime.utcnow() + timedelta(minutes=15) # Tiempo por defecto si no se manda uno
    datos_copia.update({"exp": expiracion}) # Agregamos la fecha de expiración al contenido del token
    return jwt.encode(datos_copia, SECRET_KEY, algorithm=ALGORITHM) # Encriptamos todo y devolvemos el texto del token

# Función que se encarga de validar el token enviado por el usuario
async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    try:
        # Intentamos desencriptar el token con nuestra llave secreta
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario: str = payload.get("sub") # Extraemos el nombre de usuario (el "sub")
        if usuario is None:
            # Si el token no trae usuario, mandamos error de no autorizado
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="token no válido",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return usuario # Si todo está bien, regresamos el nombre del usuario
    except JWTError:
        # Si el token está mal escrito o ya expiró, mandamos este error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token expirado o no válido",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Ruta para que el usuario inicie sesión y reciba su token
@app.post("/token", tags=['Seguridad'])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Verificamos si el usuario y contraseña son los correctos (están fijos aquí)
    if form_data.username == "Joshua" and form_data.password == "Contrasena1212":
        tiempo_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) # Definimos cuánto durará
        token_acceso = crear_token_acceso(
            datos={"sub": form_data.username}, tiempo_expiracion=tiempo_token
        ) # Creamos el token
        return {"access_token": token_acceso, "token_type": "bearer"} # Entregamos el token al cliente
    else:
        # Si los datos están mal, avisamos que no tiene permiso
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Ruta simple para probar que la api está viva
@app.get("/", tags = ['Inicio'])
async def bienvenido():
    return {"Mensaje": "Bienvenido a FastAPI con JWT"}

# Nuestra "base de datos" temporal en memoria
usuarios = [
    {"id":1, "nombre":"Jorge", "edad":"20"},
    {"id":2, "nombre":"Beto Normal", "edad":"20"},
    {"id":3, "nombre":"Cris", "edad":"22"},
    {"id":4, "nombre":"Lalo", "edad":"20"}
]

# Reglas de cómo debe ser la información de un usuario
class crear_usuario(BaseModel):
    id: int = Field(..., gt = 0) # El id debe ser un número entero mayor a 0
    nombre: str = Field(..., min_length = 3, max_length = 50) # El nombre debe tener entre 3 y 50 letras
    edad: int = Field(..., min_length = 1, max_length = 125) # Edad lógica entre 1 y 125

# Buscar un usuario por su id usando la dirección url directamente
@app.get("/v1/ParametroOb/{id}", tags = ['Parámetro obligatorio'])
async def consultauno(id:int):
    return {"Mensaje": "Usuario encontrado", "Usuario": id, "Status": "200"}

# Consultar usuarios usando parámetros opcionales detrás del signo ?
@app.get("/v1/ParametroOp/", tags = ['Parámetro opcional'])
async def consultatodos(id:Optional[int] = None):
    if id is not None:
        # Si mandaron un id, lo buscamos en la lista
        for usuarioK in usuarios:
            if usuarioK["id"] == id:
                return{"Mensaje": "Usuario encontrado", "Usuario": usuarioK, "Status": "200"}
        return{"Mensaje": "Usuario no encontrado", "Status": "200"}
    else:
        # Si no mandaron nada, solo avisamos
        return {"Mensaje":"No se proporcionó ID"}

# Ver la lista completa de todos los usuarios
@app.get("/v1/usuarios/", tags = ['Crud http'])
async def consultaT():
    return{
        "status": "200",
        "total": len(usuarios),
        "Usuarios": usuarios
    }

# Registrar un nuevo usuario en la lista
@app.post("/v1/usuarios/", tags = ['Crud http'])
async def agregar_usuario(usuario: crear_usuario):
    for usr in usuarios:
        # Revisamos que el ID no esté ya ocupado
        if usr["id"] == usuario.id:
            raise HTTPException(status_code = 400, detail = "El id ya existe.")
    usuarios.append(usuario) # Lo agregamos a la lista
    return {"Mensaje" : "Usuario agregado", "Usuario" : usuario, "Status" : "200"}

# Modificar un usuario. Esta ruta está PROTEGIDA con token.
@app.put("/v1/usuarios/{id}", tags = ['Crud http'])
async def actualizar_usuario(id: int, usuario_actualizado: dict, token: str = Depends(obtener_usuario_actual)):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios[index].update(usuario_actualizado) # Actualizamos los datos
            return {"Mensaje": "Usuario actualizado", "Usuario": usuarios[index], "Status": "200"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado") # Si no existía el ID

# Eliminar un usuario. También requiere que el token sea válido.
@app.delete("/v1/usuarios/{id}", tags = ['Crud http'])
async def eliminar_usuario(id: int, token: str = Depends(obtener_usuario_actual)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr) # Lo sacamos de la lista
            return {"Mensaje": f"Usuario eliminado por {token}", "Status": "200"}
    raise HTTPException(status_code = 404, detail="Usuario no encontrado")