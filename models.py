
from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Equipo(Base):
    __tablename__ = "equipos"

    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    tipo = Column(String)
    marca = Column(String)
    modelo = Column(String)
    serie = Column(String)
    ubicacion = Column(String)
    fecha_adquisicion = Column(DateTime)
    estado_operativo = Column(Boolean)

    contrato = Column(String)  
    proveedor = Column(String)  
    prioridad_mtto = Column(String)  
    frecuencia_mtto = Column(String)

class Mantenimiento(Base):
    __tablename__ = 'mantenimientos'
    id = Column(Integer, primary_key=True, index=True)
    id_equipo = Column(Integer)
    tipo = Column(String)
    fecha_programada = Column(DateTime)
    fecha_realizada = Column(DateTime, nullable=True)  
    tecnico = Column(String)
    observaciones = Column(Text)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nombre = Column(String)
    correo = Column(String, unique=True)
    rol = Column(String)
    contraseña_encriptada = Column(String)

class HistorialOperatividad(Base):
    __tablename__ = 'historial_operatividad'
    id = Column(Integer, primary_key=True)
    id_equipo = Column(Integer, ForeignKey('equipos.id'))
    fecha_hora = Column(DateTime)
    estado = Column(Boolean)