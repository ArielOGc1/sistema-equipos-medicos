
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # Importa Base desde models

SQLALCHEMY_DATABASE_URL = "sqlite:///./base_datos.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()