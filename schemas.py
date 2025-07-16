
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EquipoBase(BaseModel):
    nombre: str
    tipo: str
    marca: str
    modelo: str
    serie: str
    ubicacion: str
    fecha_adquisicion: datetime
    estado_operativo: bool
    contrato: str
    proveedor: str
    prioridad_mtto: str
    frecuencia_mtto: str

class EquipoCrear(EquipoBase):
    pass

class EquipoMostrar(EquipoBase):
    id: int

    class Config:
        from_attributes = True

class MantenimientoBase(BaseModel):
    id_equipo: int
    tipo: str
    fecha_programada: datetime
    fecha_realizada: Optional[datetime] = None  
    tecnico: str
    observaciones: Optional[str] = None
    
    class Config:
        from_attributes = True

class MantenimientoCrear(MantenimientoBase):
    pass

class MantenimientoMostrar(MantenimientoBase):
    id: int

    class Config:
        from_attributes = True

class UsuarioBase(BaseModel):
    nombre: str
    correo: str
    rol: str
    contraseña_encriptada: str

class UsuarioCrear(UsuarioBase):
    pass

class UsuarioMostrar(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class HistorialBase(BaseModel):
    id_equipo: int
    fecha_hora: datetime
    estado: bool

class HistorialCrear(HistorialBase):
    pass

class HistorialMostrar(HistorialBase):
    id: int

    class Config:
        from_attributes = True