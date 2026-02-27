from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Literal
from datetime import datetime

app = FastAPI(
    title="API Biblioteca Digital",
    description="Por: Andrés Joshua León Barranco",
    version="1.0"
)

# Lista de libros para empezar con algo de información
libros = [
    {
        "id": 1,
        "titulo": "Los cuatro acuerdos",
        "autor": "Miguel Ruiz",
        "anio": 1997,
        "paginas": 160,
        "estado": "disponible"
    },
    {
        "id": 2,
        "titulo": "El principito",
        "autor": "Antoine de Saint-Exupéry",
        "anio": 1943,
        "paginas": 96,
        "estado": "disponible"
    }
]

# Lista para guardar los prestamos que se vayan haciendo
prestamos = []

# Definimos como debe ser un libro
class Libro(BaseModel):
    id: int
    titulo: str = Field(..., min_length=2, max_length=100)
    autor: str
    anio: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    estado: Literal["disponible", "prestado"] = "disponible"

# Definimos los datos del usuario
class Usuario(BaseModel):
    nombre: str
    correo: EmailStr

# Definimos que datos lleva un prestamo
class Prestamo(BaseModel):
    id_prestamo: int
    id_libro: int
    usuario: Usuario

# Ruta para agregar un libro nuevo
@app.post("/v1/libros", status_code=status.HTTP_201_CREATED, tags=['Libros'])
async def registrar_libro(libro: Libro):
    # Revisamos que el ID no este repetido
    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El id ya existe"
            )
    # Agregamos el libro a nuestra lista
    libros.append(libro.model_dump())
    return {"mensaje": "Libro registrado", "libro": libro}

# Ruta para ver todos los libros que tenemos
@app.get("/v1/libros", tags=['Libros'])
async def listar_libros():
    return {"libros": libros}

# Ruta para buscar un libro por su titulo
@app.get("/v1/libros/buscar/{nombre}", tags=['Libros'])
async def buscar_libro(nombre: str):
    # Buscamos el nombre dentro de la lista de libros
    resultado = [l for l in libros if nombre.lower() in l["titulo"].lower()]
    return {"resultados": resultado}

# Ruta para prestar un libro
@app.post("/v1/prestamos", status_code=status.HTTP_201_CREATED, tags=['Préstamos'])
async def registrar_prestamo(prestamo: Prestamo):
    # Buscamos si el libro existe
    libro = next((l for l in libros if l["id"] == prestamo.id_libro), None)
    
    if not libro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El libro solicitado no existe"
        )
    
    # Checamos si no esta prestado ya
    if libro["estado"] == "prestado":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="El libro ya se encuentra prestado"
        )
    
    # Cambiamos el estado a prestado y lo guardamos
    libro["estado"] = "prestado"
    prestamos.append(prestamo)
    return {"mensaje": "Préstamo registrado exitosamente"}

# Ruta para cuando devuelven un libro
@app.put("/v1/libros/devolver/{id_libro}", tags=['Préstamos'])
async def devolver_libro(id_libro: int):
    # Buscamos el prestamo en la lista
    prestamo_act = next((p for p in prestamos if p.id_libro == id_libro), None)
    
    if not prestamo_act:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="No existe un registro de préstamo activo para este libro"
        )
    
    # Ponemos el libro como disponible otra vez
    libro = next((l for l in libros if l["id"] == id_libro), None)
    libro["estado"] = "disponible"
    # Quitamos el prestamo de la lista
    prestamos.remove(prestamo_act)
    return {"mensaje": "Libro devuelto correctamente"}

# Ruta para borrar un prestamo de la lista
@app.delete("/v1/prestamos/{id_prestamo}", tags=['Préstamos'])
async def eliminar_prestamo(id_prestamo: int):
    # Buscamos el prestamo por su ID para borrarlo
    prestamo = next((p for p in prestamos if p.id_prestamo == id_prestamo), None)
    
    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Préstamo no encontrado"
        )
        
    prestamos.remove(prestamo)
    return {"mensaje": "Registro de préstamo eliminado"}