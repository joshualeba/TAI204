from fastapi.security import HTTPBasic, HTTPBasicCredentials # Para el inicio de sesión básico
import secrets # Para comparar contraseñas de forma segura
from fastapi import status, HTTPException, Depends # Importamos las bases de FastAPI y dependencias

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