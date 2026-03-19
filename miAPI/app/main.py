from fastapi import FastAPI, APIRouter
from app.routers import usuarios, varios

# Iniciamos nuestra primera API
app = FastAPI(
    title = "Mi Primera API", # Nombre del proyecto
    description = "Andrés Joshua León Barranco", # Autor
    version = "1.0" # Versión inicial
)

app.include_router(usuarios.router)
app.include_router(varios.routerV)