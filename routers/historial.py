
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import HistorialOperatividad
from schemas import HistorialCrear, HistorialMostrar
from database import get_db

router = APIRouter(prefix="/historial", tags=["historial_operatividad"])

@router.post("/", response_model=HistorialMostrar)
def crear_historial(historial: HistorialCrear, db: Session = Depends(get_db)):
    nuevo = HistorialOperatividad(**historial.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[HistorialMostrar])
def obtener_historial(db: Session = Depends(get_db)):
    return db.query(HistorialOperatividad).all()

@router.get("/{historial_id}", response_model=HistorialMostrar)
def obtener_estado(historial_id: int, db: Session = Depends(get_db)):
    h = db.query(HistorialOperatividad).filter(HistorialOperatividad.id == historial_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return h

@router.put("/{historial_id}", response_model=HistorialMostrar)
def actualizar_estado(historial_id: int, datos: HistorialCrear, db: Session = Depends(get_db)):
    h = db.query(HistorialOperatividad).filter(HistorialOperatividad.id == historial_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    for attr, value in datos.dict().items():
        setattr(h, attr, value)
    db.commit()
    db.refresh(h)
    return h

@router.delete("/{historial_id}")
def eliminar_estado(historial_id: int, db: Session = Depends(get_db)):
    h = db.query(HistorialOperatividad).filter(HistorialOperatividad.id == historial_id).first()
    if not h:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    db.delete(h)
    db.commit()
    return {"mensaje": "Historial eliminado correctamente"}