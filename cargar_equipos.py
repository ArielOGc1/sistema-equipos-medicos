
from datetime import datetime
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Equipo
import random

prioridades = ["Alta", "Media", "Baja"]
frecuencias = ["Mensual", "Trimestral", "Semestral", "Anual"]

# Mapeo de ubicaciones realistas
equipos = [
    {"nombre": "Mesa de Autopsia", "marca": "Nacional", "modelo": "FO-MA1", "serie": "N/A", "contrato": "42-2015", "proveedor": "RECOR DENTAL", "ubicacion": "Patología"},
    {"nombre": "Mesa de Manos y Tendones", "marca": "Nacional", "modelo": "N/A", "serie": "N/A", "contrato": "78-2015", "proveedor": "MALBO", "ubicacion": "Quirófano"},
    {"nombre": "Mesa de Operaciones", "marca": "UZUMCO", "modelo": "OM-8P", "serie": "11149004020", "contrato": "64-2014", "proveedor": "ODELGA MED", "ubicacion": "Quirófano"},
    {"nombre": "Mesa de Procedimientos", "marca": "MIDMARK", "modelo": "630-020", "serie": "V1605436", "contrato": "64-2015", "proveedor": "DT MEDICAL", "ubicacion": "Consulta Externa"},
    {"nombre": "Mezclador de Tubos", "marca": "F NUTATOR", "modelo": "N-2336", "serie": "VL2005", "contrato": "N/A", "proveedor": "DISTRITO 17D02 SALUD", "ubicacion": "Laboratorio"},
    {"nombre": "Microscopio", "marca": "HUMAN DIAGNOSTIC", "modelo": "HUMASCOPE LIGHT", "serie": "112014", "contrato": "AD2017-005", "proveedor": "FRISONEX CIA LTDA", "ubicacion": "Laboratorio"},
    {"nombre": "Microscopio Binocular", "marca": "LW SCIENTIFIC", "modelo": "REVELATION III", "serie": "141443", "contrato": "9-2015", "proveedor": "MEDILABOR S.A.", "ubicacion": "Laboratorio"},
    {"nombre": "Microscopio Otorrinolaringología", "marca": "ECLERIS", "modelo": "OM100", "serie": "UM10M10FR9000007", "contrato": "AD2017-031", "proveedor": "COMRE", "ubicacion": "Consulta Externa"},
    {"nombre": "Microscopio Patología", "marca": "NIKON", "modelo": "CI-L", "serie": "709142", "contrato": "AD2017-056", "proveedor": "RECOR DENTAL", "ubicacion": "Patología"},
    {"nombre": "Microtomo", "marca": "AMERICAN OPTICAL", "modelo": "OPTICA 820", "serie": "70754", "contrato": "N/A", "proveedor": "HOSPITAL DERMATOLÓGICO", "ubicacion": "Patología"},
    {"nombre": "Monitor Signos Intermedio", "marca": "CONTEC", "modelo": "CMS 8000", "serie": "20060400123", "contrato": "118-2020 BID", "proveedor": "PROYECTO BID", "ubicacion": "Hospitalización"},
    {"nombre": "Monitor Intraparto", "marca": "EDAN", "modelo": "F9 EXPRESS", "serie": "M15100590009", "contrato": "138-2014", "proveedor": "CHINA SINOPHARM", "ubicacion": "Ginecología"},
    {"nombre": "Monitor Multiparámetro", "marca": "MINDRAY", "modelo": "BENEVIEW T8", "serie": "CF-54162233", "contrato": "138-2014", "proveedor": "CHINA SINOPHARM", "ubicacion": "UCI"},
    {"nombre": "Nebulizador Compresor", "marca": "ALLIED", "modelo": "T14614", "serie": "20140903008", "contrato": "77A-2015", "proveedor": "DT MEDICAL", "ubicacion": "Consulta Externa"},
    {"nombre": "Otoscopio-Oftalmoscopio", "marca": "RIESTER", "modelo": "RI-FORMER", "serie": "N/A", "contrato": "64-2014", "proveedor": "ODELGA MED", "ubicacion": "Consulta Externa"},
    {"nombre": "Pesabebe Digital", "marca": "RICE LAKE", "modelo": "RL-DBS", "serie": "15061300448", "contrato": "2015-003", "proveedor": "MEDICAL DOCTORS", "ubicacion": "Neonatología"},
    {"nombre": "Set Laringoscopio Adulto", "marca": "PROPPER", "modelo": "N/A", "serie": "US PAT 5542905", "contrato": "2015-258", "proveedor": "MEDICAL DOCTORS", "ubicacion": "Emergencia"},
    {"nombre": "Sillón Ginecológico", "marca": "COMBED", "modelo": "DH-S102C", "serie": "15-2177", "contrato": "138-2014", "proveedor": "CHINA SINOPHARM", "ubicacion": "Ginecología"},
    {"nombre": "TENS Dos Canales", "marca": "I-TECH", "modelo": "T-ONE PHYSIO", "serie": "09218/14", "contrato": "78-2015", "proveedor": "MALBO", "ubicacion": "Fisioterapia"},
    {"nombre": "Torre de Imagen", "marca": "FUJIFILM", "modelo": "N/A", "serie": "K514A0093", "contrato": "19-2015", "proveedor": "TOP MEDICAL", "ubicacion": "Imagenología"},
]

db: Session = SessionLocal()

for eq in equipos:
    equipo = Equipo(
        nombre=eq["nombre"],
        tipo="Diagnóstico",  # Puedes personalizarlo también si lo deseas
        marca=eq["marca"],
        modelo=eq["modelo"],
        serie=eq["serie"],
        ubicacion=eq["ubicacion"],
        fecha_adquisicion=datetime(2020, 1, 1),
        estado_operativo=random.choice([True, False]),
        contrato=eq["contrato"],
        proveedor=eq["proveedor"],
        prioridad_mtto=random.choice(prioridades),
        frecuencia_mtto=random.choice(frecuencias)
    )
    db.add(equipo)

db.commit()
db.close()
print("✅ Equipos agregados con ubicaciones realistas.")