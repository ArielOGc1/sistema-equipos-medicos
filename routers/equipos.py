
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Equipo
from schemas import EquipoCrear, EquipoMostrar
from database import get_db

router = APIRouter(prefix="/equipos", tags=["equipos"])

# 🔍 Filtrar por prioridad
@router.get("/por_prioridad/{nivel}", response_model=list[EquipoMostrar])
def filtrar_por_prioridad(nivel: str, db: Session = Depends(get_db)):
    equipos = db.query(Equipo).filter(Equipo.prioridad_mtto == nivel).all()
    return equipos

# 🔍 Filtrar por frecuencia
@router.get("/por_frecuencia/{frecuencia}", response_model=list[EquipoMostrar])
def filtrar_por_frecuencia(frecuencia: str, db: Session = Depends(get_db)):
    equipos = db.query(Equipo).filter(Equipo.frecuencia_mtto == frecuencia).all()
    return equipos

# 🔍 Equipos operativos
@router.get("/operativos", response_model=list[EquipoMostrar])
def equipos_operativos(db: Session = Depends(get_db)):
    equipos = db.query(Equipo).filter(Equipo.estado_operativo == True).all()
    return equipos

# 🔍 Equipos en avería
@router.get("/en_averia", response_model=list[EquipoMostrar])
def equipos_averiados(db: Session = Depends(get_db)):
    equipos = db.query(Equipo).filter(Equipo.estado_operativo == False).all()
    return equipos

@router.post("/", response_model=EquipoMostrar)
def crear_equipo(equipo: EquipoCrear, db: Session = Depends(get_db)):
    nuevo = Equipo(**equipo.dict())
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@router.get("/", response_model=list[EquipoMostrar])
def obtener_equipos(db: Session = Depends(get_db)):
    return db.query(Equipo).all()

@router.get("/{equipo_id}", response_model=EquipoMostrar)
def obtener_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo = db.query(Equipo).filter(Equipo.id == equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    return equipo


@router.put("/{equipo_id}", response_model=EquipoMostrar)
def actualizar_equipo(equipo_id: int, datos: EquipoCrear, db: Session = Depends(get_db)):
    equipo = db.query(Equipo).filter(Equipo.id == equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    for attr, value in datos.dict().items():
        setattr(equipo, attr, value)
    db.commit()
    db.refresh(equipo)
    return equipo


@router.delete("/{equipo_id}")
def eliminar_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo = db.query(Equipo).filter(Equipo.id == equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")
    db.delete(equipo)
    db.commit()
    return {"mensaje": "Equipo eliminado correctamente"}

