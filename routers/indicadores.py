
import math
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Equipo, Mantenimiento
from database import get_db

router = APIRouter(prefix="/indicadores", tags=["indicadores"])

@router.get("/resumen")
def indicadores_generales(db: Session = Depends(get_db)):
    total_equipos = db.query(Equipo).count()
    equipos_inactivos = db.query(Equipo).filter(Equipo.estado_operativo == False).count()
    equipos_operativos = total_equipos - equipos_inactivos

    # 🛠 Obtener todos los mantenimientos con fechas válidas
    mantenimientos = db.query(Mantenimiento).filter(
        Mantenimiento.fecha_programada != None,
        Mantenimiento.fecha_realizada != None
    ).all()

    total_reparaciones = len(mantenimientos)

    total_tiempo_reparacion = sum([
        (m.fecha_realizada - m.fecha_programada).total_seconds() / 3600
        for m in mantenimientos
    ])

    # 🔹 Supongamos que los equipos funcionan las 24 horas por 7 días
    total_funcionamiento = total_equipos * 7 * 24

    # MTBF: tiempo medio entre fallas (en base a cantidad de fallas)
    numero_fallas = equipos_inactivos
    mtbf = (total_funcionamiento / numero_fallas) if numero_fallas > 0 else 0

    # MTTR: tiempo medio para reparación
    mttr = (total_tiempo_reparacion / total_reparaciones) if total_reparaciones > 0 else 0

    # Disponibilidad: porcentaje de tiempo útil
    paradas_no_programadas = 4  # simuladas, podrías hacerlo real si registras esas horas
    disponibilidad = (mtbf / (mtbf + mttr + paradas_no_programadas)) * 100 if (mtbf + mttr + paradas_no_programadas) > 0 else 0

    # Confiabilidad: e^(-λt), λ = 1 / MTBF
    t = 7 * 24  # tiempo analizado en horas
    landa = 1 / mtbf if mtbf > 0 else 0
    confiabilidad = math.exp(-landa * t)

    # 🔸 Simulados por ahora (puedes volver esto real en el futuro)
    procesos_teoricos = 40
    procesos_reales = 34
    defectuosos = 3

    rendimiento = (procesos_reales / procesos_teoricos) * 100 if procesos_teoricos else 0
    calidad = ((procesos_reales - defectuosos) / procesos_reales) * 100 if procesos_reales else 0

    # OEE: Disponibilidad * Rendimiento * Calidad
    oee = (disponibilidad * rendimiento * calidad) / 10000

    return {
        "total_equipos": total_equipos,
        "equipos_operativos": equipos_operativos,
        "equipos_en_averia": equipos_inactivos,
        "MTBF (horas)": round(mtbf, 2),
        "MTTR (horas)": round(mttr, 2),
        "Disponibilidad (%)": round(disponibilidad, 2),
        "Confiabilidad": round(confiabilidad, 4),
        "Rendimiento (%)": round(rendimiento, 2),
        "Calidad (%)": round(calidad, 2),
        "OEE (%)": round(oee, 2)
    }


# 🔹 /equipos/resumen
@router.get("/equipos/resumen")
def resumen_equipos(db: Session = Depends(get_db)):
    equipos = db.query(Equipo).all()
    return [
        {
            "id": e.id,
            "nombre": e.nombre,
            "tipo": e.tipo,
            "estado_operativo": e.estado_operativo,
            "ubicacion": e.ubicacion
        }
        for e in equipos
    ]


# 🔹 /equipos/{id}/detalles
@router.get("/equipos/{equipo_id}/detalles")
def detalles_equipo(equipo_id: int, db: Session = Depends(get_db)):
    equipo = db.query(Equipo).filter(Equipo.id == equipo_id).first()
    if not equipo:
        raise HTTPException(status_code=404, detail="Equipo no encontrado")

    return {
        "id": equipo.id,
        "nombre": equipo.nombre,
        "marca": equipo.marca,
        "modelo": equipo.modelo,
        "serie": equipo.serie,
        "ubicacion": equipo.ubicacion,
        "fecha_adquisicion": equipo.fecha_adquisicion,
        "estado_operativo": equipo.estado_operativo,
        "tipo": equipo.tipo,
        "frecuencia_mantenimiento": equipo.frecuencia_mtto,
        "prioridad": equipo.prioridad_mtto,
        "responsable": "Técnico 1",  # simulado
        "proveedor": equipo.proveedor,
        "contrato": equipo.contrato
    }

