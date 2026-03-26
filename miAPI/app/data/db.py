from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv( # corregido de os.getch
    "DATABASE_URL",
    "postgresql://admin:123456@postgres:5432/DB_miapi"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base() # Esta es la Base que importarás en main.py

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()