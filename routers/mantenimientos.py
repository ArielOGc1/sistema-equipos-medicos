
from fastapi import APIRouter, Depends, HTTPException, Path, Body
from sqlalchemy.orm import Session
from models import Mantenimiento
from schemas import MantenimientoCrear, MantenimientoMostrar, MantenimientoBase
from database import get_db
from datetime import datetime, timedelta

router = APIRouter(prefix="/mantenimientos", tags=["mantenimientos"])

@router.post("/")
def crear_mantenimiento(mantenimiento: MantenimientoBase, db: Session = Depends(get_db)):
    nuevo = Mantenimiento(
        id_equipo=mantenimiento.id_equipo,
        tipo=mantenimiento.tipo,
        fecha_programada=mantenimiento.fecha_programada,
        fecha_realizada=mantenimiento.fecha_realizada,
        tecnico=mantenimiento.tecnico,
        observaciones=mantenimiento.observaciones
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[MantenimientoMostrar])
def obtener_mantenimientos(db: Session = Depends(get_db)):
    return db.query(Mantenimiento).all()

@router.get("/{mantenimiento_id}", response_model=MantenimientoMostrar)
def obtener_mantenimiento(mantenimiento_id: int, db: Session = Depends(get_db)):
    m = db.query(Mantenimiento).filter(Mantenimiento.id == mantenimiento_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    return m

@router.put("/{mantenimiento_id}", response_model=MantenimientoMostrar)
def actualizar_mantenimiento(mantenimiento_id: int, datos: MantenimientoCrear, db: Session = Depends(get_db)):
    m = db.query(Mantenimiento).filter(Mantenimiento.id == mantenimiento_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    for attr, value in datos.dict().items():
        setattr(m, attr, value)
    db.commit()
    db.refresh(m)
    return m

@router.delete("/{mantenimiento_id}")
def eliminar_mantenimiento(mantenimiento_id: int, db: Session = Depends(get_db)):
    m = db.query(Mantenimiento).filter(Mantenimiento.id == mantenimiento_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")
    db.delete(m)
    db.commit()
    return {"mensaje": "Mantenimiento eliminado correctamente"}

@router.get("/equipo/{equipo_id}")
def mantenimientos_por_equipo(equipo_id: int, db: Session = Depends(get_db)):
    datos = db.query(Mantenimiento).filter(Mantenimiento.id_equipo == equipo_id).all()
    if not datos:
        raise HTTPException(status_code=404, detail="No se encontraron mantenimientos para este equipo")
    return datos

@router.get("/proximos/")
def mantenimientos_proximos(dias: int = 15, db: Session = Depends(get_db)):
    hoy = datetime.now().date()
    limite = hoy + timedelta(days=dias)

    mantenimientos = db.query(Mantenimiento).filter(
        Mantenimiento.fecha_programada >= hoy,
        Mantenimiento.fecha_programada <= limite,
        Mantenimiento.fecha_realizada == None  # Solo pendientes
    ).all()

    return mantenimientos


@router.put("/realizar/{mantenimiento_id}")
def marcar_como_realizado(
    mantenimiento_id: int = Path(...),
    fecha: datetime = Body(...),
    db: Session = Depends(get_db)
):
    mantenimiento = db.query(Mantenimiento).filter(Mantenimiento.id == mantenimiento_id).first()
    if not mantenimiento:
        raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")

    mantenimiento.fecha_realizada = fecha
    db.commit()
    db.refresh(mantenimiento)
    return {"message": "Mantenimiento marcado como realizado"}