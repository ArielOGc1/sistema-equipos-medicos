
# 🏥 Sistema de Gestión de Equipos Médicos

Proyecto final de Ingeniería Clínica - UPS (Julio 2025)  
Autor: Ariel Ortega, Kevin Chochos

## 🔧 Funcionalidades principales
- Registro, edición y eliminación de equipos médicos
- Gestión de usuarios y mantenimientos
- Cálculo de indicadores técnicos:
  - ✅ MTBF y MTTR basados en datos reales
  - ✅ Disponibilidad y Confiabilidad calculados en base a MTBF y MTTR
  - ⚠️ OEE, Calidad y Rendimiento con valores simulados (opcionalmente ajustables)
- Filtros avanzados y visualización por criterios
- Exportación a Excel
- Carga de hoja de servicio en formato PDF
- Interfaz visual construida con Streamlit

## 📊 Indicadores calculados
- **MTBF** y **MTTR** se calculan con datos reales de la base de datos.
- Otros indicadores como **Disponibilidad, Confiabilidad, Rendimiento, Calidad y OEE** utilizan datos simulados o parcialmente simulados para su cálculo.

## 🚀 Requisitos
- Python 3.9+
- Instalar dependencias: `pip install -r requirements.txt`

## ▶️ Cómo ejecutar
1. Ejecuta el backend:
```bash
uvicorn main:app --reload
```

2. Ejecuta el frontend:
```bash
streamlit run app.py
```

## 🧠 Notas
- El sistema usa SQLite (local)
- Las hojas de servicio se almacenan localmente en la carpeta `/archivos`
- Indicadores se recalculan dinámicamente en base a los datos actuales
