from fastapi import FastAPI, status, HTTPException # Herramientas principales de nuestra API
from pydantic import BaseModel, Field, EmailStr # Para definir las formas de nuestros datos y validar correos
from typing import List, Optional, Literal # Herramientas para tipos de datos más específicos
from datetime import datetime # Para manejar la fecha actual

# Iniciamos nuestra aplicación de la biblioteca
app = FastAPI(
    title="API Biblioteca Digital", # Título que se ve en la web
    description="Por: Andrés Joshua León Barranco", # Autor
    version="1.0" # Versión del programa
)

# Lista inicial de libros para que no esté vacía al empezar
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

# Lista para llevar el registro de quién se lleva qué libro
prestamos = []

# Definimos las reglas que debe cumplir un libro para ser aceptado
class Libro(BaseModel):
    id: int # Identificador único numérico
    titulo: str = Field(..., min_length=2, max_length=100) # Título de entre 2 y 100 letras
    autor: str # Nombre de quien lo escribió
    anio: int = Field(..., gt=1450, le=datetime.now().year) # El año debe ser lógico (no antes de 1450 ni en el futuro)
    paginas: int = Field(..., gt=1) # Debe tener al menos una página
    estado: Literal["disponible", "prestado"] = "disponible" # Solo puede estar en uno de estos dos estados

# Definimos cómo es un usuario que quiere un libro
class Usuario(BaseModel):
    nombre: str # Su nombre completo
    correo: EmailStr # Su correo (Pydantic validará que sea un correo real)

# Definimos la estructura de un registro de préstamo
class Prestamo(BaseModel):
    id_prestamo: int # Número de folio del préstamo
    id_libro: int # Cuál libro se están llevando
    usuario: Usuario # Quién se lo lleva (reutilizamos la clase Usuario)

# Ruta para meter un libro nuevo al sistema
@app.post("/v1/libros", status_code=status.HTTP_201_CREATED, tags=['Libros'])
async def registrar_libro(libro: Libro):
    # Revisamos que no intenten meter un ID que ya existe
    for l in libros:
        if l["id"] == libro.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El id ya existe"
            )
    # Si todo está bien, lo agregamos a nuestra lista
    libros.append(libro.model_dump())
    return {"mensaje": "Libro registrado", "libro": libro}

# Ruta para ver el catálogo completo de libros
@app.get("/v1/libros", tags=['Libros'])
async def listar_libros():
    return {"libros": libros}

# Ruta para buscar libros por una parte de su nombre
@app.get("/v1/libros/buscar/{nombre}", tags=['Libros'])
async def buscar_libro(nombre: str):
    # Buscamos coincidencias ignorando mayúsculas y minúsculas
    resultado = [l for l in libros if nombre.lower() in l["titulo"].lower()]
    return {"resultados": resultado}

# Ruta para marcar un libro como prestado
@app.post("/v1/prestamos", status_code=status.HTTP_201_CREATED, tags=['Préstamos'])
async def registrar_prestamo(prestamo: Prestamo):
    # Buscamos si el libro que quieren realmente existe en nuestra lista
    libro = next((l for l in libros if l["id"] == prestamo.id_libro), None)
    
    if not libro:
        # Si no lo encontramos, avisamos que no existe
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="El libro solicitado no existe"
        )
    
    # Si sí existe, checamos si ya se lo llevó alguien más
    if libro["estado"] == "prestado":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="El libro ya se encuentra prestado"
        )
    
    # Si está disponible, lo marcamos como prestado y guardamos el registro
    libro["estado"] = "prestado"
    prestamos.append(prestamo)
    return {"mensaje": "Préstamo registrado exitosamente"}

# Ruta para marcar que un libro ya regresó a la biblioteca
@app.put("/v1/libros/devolver/{id_libro}", tags=['Préstamos'])
async def devolver_libro(id_libro: int):
    # Buscamos si hay un préstamo activo para ese libro
    prestamo_act = next((p for p in prestamos if p.id_libro == id_libro), None)
    
    if not prestamo_act:
        # Si no hay registro de que alguien se lo llevó, mandamos error
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail="No existe un registro de préstamo activo para este libro"
        )
    
    # Buscamos el libro y lo ponemos como disponible de nuevo
    libro = next((l for l in libros if l["id"] == id_libro), None)
    libro["estado"] = "disponible"
    # Quitamos el papel del préstamo de nuestra lista
    prestamos.remove(prestamo_act)
    return {"mensaje": "Libro devuelto correctamente"}

# Ruta para borrar un registro de préstamo (limpiar historial)
@app.delete("/v1/prestamos/{id_prestamo}", tags=['Préstamos'])
async def eliminar_prestamo(id_prestamo: int):
    # Lo buscamos por su número de folio
    prestamo = next((p for p in prestamos if p.id_prestamo == id_prestamo), None)
    
    if not prestamo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Préstamo no encontrado"
        )
        
    prestamos.remove(prestamo) # Lo borramos de la lista
    return {"mensaje": "Registro de préstamo eliminado"}