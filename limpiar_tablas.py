
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Mantenimiento, Usuario, HistorialOperatividad, Equipo

db: Session = SessionLocal()

# Borrar datos de tablas dinámicas
db.query(Mantenimiento).delete()
db.query(Usuario).delete()
db.query(HistorialOperatividad).delete()
db.query(Equipo).delete()

db.commit()
db.close()

print("✅ Tablas limpiadas correctamente.")