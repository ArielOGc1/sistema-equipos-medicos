
from fastapi import FastAPI
from sqlalchemy import create_engine
from models import Base
from routers import equipos, mantenimientos, usuarios, historial, archivos
from routers import indicadores  

# uvicorn main:app --reload

app = FastAPI()

engine = create_engine('sqlite:///base_datos.db')
Base.metadata.create_all(engine)

app.include_router(equipos.router)
app.include_router(mantenimientos.router)
app.include_router(usuarios.router)
app.include_router(historial.router)
app.include_router(indicadores.router)
app.include_router(archivos.router)

@app.get("/")
def home():
    return {"message": "API de clínica operativa"}

