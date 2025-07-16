
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from models import Mantenimiento
from database import get_db
import os
import shutil

router = APIRouter(prefix="/archivos", tags=["archivos"])

ARCHIVOS_DIR = "archivos"
os.makedirs(ARCHIVOS_DIR, exist_ok=True)

@router.post("/subir_hoja/{mantenimiento_id}")
def subir_hoja_servicio(mantenimiento_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    mantenimiento = db.query(Mantenimiento).filter(Mantenimiento.id == mantenimiento_id).first()
    if not mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")

    # Guardar el archivo en la carpeta local sin modificar la base de datos
    ruta = os.path.join(ARCHIVOS_DIR, f"hoja_servicio_{mantenimiento_id}.pdf")
    with open(ruta, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": "Hoja de servicio guardada en servidor", "archivo": ruta}