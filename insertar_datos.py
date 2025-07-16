
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from models import Base, Equipo, Mantenimiento, Usuario, HistorialOperatividad

# Conectarse a la base de datos
engine = create_engine('sqlite:///base_datos.db')
Session = sessionmaker(bind=engine)
session = Session()

# =========================
# INSERTAR EQUIPOS
# =========================
equipo1 = Equipo(
    nombre="Desfibrilador",
    tipo="Emergencia",
    marca="Philips",
    modelo="HeartStart",
    serie="DF12345",
    ubicacion="Sala de urgencias",
    fecha_adquisicion=datetime(2022, 5, 10),
    estado_operativo=True
)

equipo2 = Equipo(
    nombre="Electrocardiógrafo",
    tipo="Diagnóstico",
    marca="GE",
    modelo="MAC 2000",
    serie="ECG98765",
    ubicacion="Consulta externa",
    fecha_adquisicion=datetime(2021, 8, 15),
    estado_operativo=False
)

session.add_all([equipo1, equipo2])
session.commit()

# =========================
# INSERTAR USUARIOS
# =========================
usuario1 = Usuario(
    nombre="Juan Pérez",
    correo="juan.perez@example.com",
    rol="técnico",
    contraseña_encriptada="123456hashed"
)

usuario2 = Usuario(
    nombre="Ana Gómez",
    correo="ana.gomez@example.com",
    rol="admin",
    contraseña_encriptada="abcdefhashed"
)

session.add_all([usuario1, usuario2])
session.commit()

# =========================
# INSERTAR MANTENIMIENTOS
# =========================
mantenimiento1 = Mantenimiento(
    id_equipo=1,
    tipo="preventivo",
    fecha_programada=datetime(2023, 6, 10),
    fecha_realizada=datetime(2023, 6, 12),
    tecnico="Juan Pérez",
    observaciones="Revisión completa, sin fallos detectados"
)

session.add(mantenimiento1)
session.commit()

# =========================
# INSERTAR HISTORIAL OPERATIVIDAD
# =========================
estado1 = HistorialOperatividad(
    id_equipo=1,
    fecha_hora=datetime(2024, 6, 1, 14, 30),
    estado=True
)

estado2 = HistorialOperatividad(
    id_equipo=2,
    fecha_hora=datetime(2024, 6, 1, 15, 00),
    estado=False
)

session.add_all([estado1, estado2])
session.commit()

print("✅ Datos de prueba insertados exitosamente.")