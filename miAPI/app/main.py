from fastapi import FastAPI
from app.routers import usuarios, varios
from app.data.db import engine, Base
from app.data.usuario import Usuario # Importante para que SQLAlchemy vea el modelo

# Creamos las tablas en la base de datos al iniciar
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title = "Mi Primera API",
    description = "Andrés Joshua León Barranco",
    version = "1.0"
)

app.include_router(usuarios.router)
app.include_router(varios.routerV)