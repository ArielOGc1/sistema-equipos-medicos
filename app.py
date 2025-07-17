
import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import io
import matplotlib.pyplot as plt

# Listas para selectboxes
AREAS_EQUIPO = ["UCI", "Quirófano", "Consulta Externa", "Laboratorio", "Hospitalización", "Emergencia", "Imagenología", "Neonatología"]
TIPOS_EQUIPO = ["Diagnóstico", "Terapia", "Soporte", "Monitoreo", "Imagenología", "Laboratorio", "Otro"]

# URL del backend
API_URL = "https://backend-equipos-qv34.onrender.com"

# Configuracion de Streamlit
st.set_page_config(page_title="Inventario Médico", layout="wide")
st.title("📊 Sistema de Inventario y Mantenimiento de Equipos Médicos")

# Sidebar
st.sidebar.title("📋 Menú de funcionalidades")
menu = st.sidebar.radio("Ir a sección:", [
    "🏠 Inicio / Indicadores",
    "📋 Ver equipos",
    "➕ Agregar equipo",
    "✏️ Editar equipo",
    "🗑️ Eliminar equipo",
    "👤 Agregar usuario",
    "🎯 Filtros de equipos",
    "ℹ️ Ver detalles de equipo",
    "📥 Exportar a Excel",
    "👥 Ver y eliminar usuarios",
    "📝 Registrar mantenimiento",
    "🔎 Ver mantenimientos por equipo",
    "📝 Marcar mantenimiento como realizado",
    "📅 Próximos mantenimientos"
])

# ------------------------------
# 🏠 INICIO / INDICADORES
# ------------------------------
if menu == menu == "🏠 Inicio / Indicadores":
    st.header("📊 Dashboard general del sistema")

    equipos = requests.get(f"{API_URL}/equipos/").json()
    averiados = requests.get(f"{API_URL}/equipos/en_averia").json()
    mantenimientos = requests.get(f"{API_URL}/mantenimientos/").json()

    total_equipos = len(equipos)
    total_averiados = len(averiados)
    total_mantenimientos = len(mantenimientos)

    realizados = len([m for m in mantenimientos if m["fecha_realizada"]])
    pendientes = total_mantenimientos - realizados

    st.subheader("🔍 Estado general de los equipos y mantenimientos")

    col1, col2, col3 = st.columns(3)
    col1.metric("🩺 Total de equipos registrados", total_equipos)
    col2.metric("❌ Equipos fuera de servicio", total_averiados)
    col3.metric("🛠️ Mantenimientos programados", total_mantenimientos)

    col4, col5 = st.columns(2)
    col4.metric("✅ Mantenimientos realizados", realizados)
    col5.metric("⏳ Mantenimientos pendientes", pendientes)

    st.subheader("📐 Indicadores técnicos (automáticos)")
    indicadores = requests.get(f"{API_URL}/indicadores/resumen").json()

    col6, col7, col8 = st.columns(3)
    col6.metric("🔁 MTBF (h)", indicadores["MTBF (horas)"])
    col7.metric("🛠 MTTR (h)", indicadores["MTTR (horas)"])
    col8.metric("📊 Disponibilidad (%)", indicadores["Disponibilidad (%)"])

    col9, col10, col11 = st.columns(3)
    col9.metric("📉 Confiabilidad", indicadores["Confiabilidad"])
    col10.metric("⚡ Rendimiento (%)", indicadores["Rendimiento (%)"])
    col11.metric("🏅 OEE (%)", indicadores["OEE (%)"])

# ------------------------------
# 📋 VER EQUIPOS
# ------------------------------
elif menu == "📋 Ver equipos":
    st.header("📋 Lista de equipos registrados")
    equipos = requests.get(f"{API_URL}/equipos/").json()
    df = pd.DataFrame(equipos)
    st.dataframe(df, use_container_width=True)

# ------------------------------
# ➕ AGREGAR EQUIPO
# ------------------------------
elif menu == "➕ Agregar equipo":
    st.header("➕ Agregar nuevo equipo")
    with st.form("form_nuevo_equipo", clear_on_submit=True):
        nombre = st.text_input("Nombre del equipo")
        tipo = st.selectbox("Tipo de equipo", TIPOS_EQUIPO)
        marca = st.text_input("Marca")
        modelo = st.text_input("Modelo")
        serie = st.text_input("Serie")
        ubicacion = st.selectbox("Ubicación (area)", AREAS_EQUIPO)
        fecha = st.date_input("Fecha de adquisición")
        estado = st.selectbox("Operativo", ["Sí", "No"])
        contrato = st.text_input("Contrato")
        proveedor = st.text_input("Proveedor")
        prioridad = st.selectbox("Prioridad mantenimiento", ["Alta", "Media", "Baja"])
        frecuencia = st.selectbox("Frecuencia mantenimiento", ["Mensual", "Trimestral", "Semestral", "Anual"])
        submit = st.form_submit_button("Guardar equipo")

        if submit:
            data = {
                "nombre": nombre,
                "tipo": tipo,
                "marca": marca or "N/A",
                "modelo": modelo or "N/A",
                "serie": serie or "N/A",
                "ubicacion": ubicacion,
                "fecha_adquisicion": f"{fecha}T00:00:00",
                "estado_operativo": True if estado == "Sí" else False,
                "contrato": contrato or "N/A",
                "proveedor": proveedor or "N/A",
                "prioridad_mtto": prioridad,
                "frecuencia_mtto": frecuencia
            }
            r = requests.post(f"{API_URL}/equipos/", json=data)
            if r.status_code == 200:
                st.success("✅ Equipo agregado")
            else:
                st.error("❌ Error al agregar equipo")
                st.json(r.json())

# ------------------------------
# ✏️ EDITAR EQUIPO
# ------------------------------
elif menu == "✏️ Editar equipo":
    st.header("✏️ Editar equipo existente")
    equipos = requests.get(f"{API_URL}/equipos/").json()
    opciones = {f"{e['nombre']} - ID {e['id']}": e["id"] for e in equipos}
    equipo_key = st.selectbox("Selecciona un equipo", opciones.keys())

    if equipo_key:
        equipo_id = opciones[equipo_key]
        equipo = requests.get(f"{API_URL}/equipos/{equipo_id}").json()

        with st.form("form_editar_equipo"):
            nombre = st.text_input("Nombre", equipo["nombre"])
            tipo = st.selectbox("Tipo", TIPOS_EQUIPO, index=TIPOS_EQUIPO.index(equipo["tipo"]) if equipo["tipo"] in TIPOS_EQUIPO else 0)
            marca = st.text_input("Marca", equipo["marca"])
            modelo = st.text_input("Modelo", equipo["modelo"])
            serie = st.text_input("Serie", equipo["serie"])
            ubicacion = st.selectbox("Ubicación", AREAS_EQUIPO, index=AREAS_EQUIPO.index(equipo["ubicacion"]) if equipo["ubicacion"] in AREAS_EQUIPO else 0)
            fecha = st.date_input("Fecha adquisición", pd.to_datetime(equipo["fecha_adquisicion"]))
            estado = st.selectbox("Estado operativo", ["Sí", "No"], index=0 if equipo["estado_operativo"] else 1)
            contrato = st.text_input("Contrato", equipo["contrato"])
            proveedor = st.text_input("Proveedor", equipo["proveedor"])
            prioridad = st.selectbox("Prioridad", ["Alta", "Media", "Baja"], index=["Alta", "Media", "Baja"].index(equipo["prioridad_mtto"]))
            frecuencia = st.selectbox("Frecuencia", ["Mensual", "Trimestral", "Semestral", "Anual"], index=["Mensual", "Trimestral", "Semestral", "Anual"].index(equipo["frecuencia_mtto"]))
            submit = st.form_submit_button("Guardar cambios")

        if submit:
            data = {
                "nombre": nombre,
                "tipo": tipo,
                "marca": marca or "N/A",
                "modelo": modelo or "N/A",
                "serie": serie or "N/A",
                "ubicacion": ubicacion,
                "fecha_adquisicion": f"{fecha}T00:00:00",
                "estado_operativo": True if estado == "Sí" else False,
                "contrato": contrato or "N/A",
                "proveedor": proveedor or "N/A",
                "prioridad_mtto": prioridad,
                "frecuencia_mtto": frecuencia
            }
            r = requests.put(f"{API_URL}/equipos/{equipo_id}", json=data)
            if r.status_code == 200:
                st.success("✅ Cambios guardados")
            else:
                st.error("❌ Error al guardar")
                st.json(r.json())

# ------------------------------
# 🗑️ ELIMINAR EQUIPO
# ------------------------------
elif menu == "🗑️ Eliminar equipo":
    st.header("🗑️ Eliminar equipo")
    equipos = requests.get(f"{API_URL}/equipos/").json()
    opciones = {f"{e['nombre']} - ID {e['id']}": e["id"] for e in equipos}
    equipo_key = st.selectbox("Selecciona equipo a eliminar", opciones.keys())

    if equipo_key:
        equipo_id = opciones[equipo_key]
        equipo = requests.get(f"{API_URL}/equipos/{equipo_id}").json()
        st.write(f"**Nombre:** {equipo['nombre']}")
        st.write(f"**Ubicación:** {equipo['ubicacion']}")
        st.write("⚠️ Esta acción es irreversible.")

        if st.button("Eliminar permanentemente"):
            r = requests.delete(f"{API_URL}/equipos/{equipo_id}")
            if r.status_code == 200:
                st.success("✅ Equipo eliminado")
                st.stop()
            else:
                st.error("❌ No se pudo eliminar")
                st.json(r.json())

# ------------------------------
# 👤 AGREGAR USUARIO
# ------------------------------
elif menu == "👤 Agregar usuario":
    st.header("👤 Agregar nuevo usuario")
    with st.form("form_usuario", clear_on_submit=True):
        nombre = st.text_input("Nombre")
        correo = st.text_input("Correo")
        rol = st.selectbox("Rol", ["Técnico", "Administrador", "Usuario"])
        contrasena = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Guardar usuario")

        if submit:
            if not nombre or not correo or not contrasena:
                st.warning("Todos los campos son obligatorios.")
            else:
                data = {
                    "nombre": nombre,
                    "correo": correo,
                    "rol": rol,
                    "contraseña_encriptada": contrasena
                }
                r = requests.post(f"{API_URL}/usuarios/", json=data)
                if r.status_code == 200:
                    st.success("✅ Usuario registrado")
                else:
                    st.error("❌ Error al registrar usuario")
                    st.json(r.json())

# ------------------------------
# 🎯 FILTROS
# ------------------------------
elif menu == "🎯 Filtros de equipos":
    st.header("🎯 Filtros de equipos")
    filtro = st.selectbox("Filtrar por:", ["Todos", "Estado", "Prioridad", "Frecuencia", "Ubicación"])
    equipos = requests.get(f"{API_URL}/equipos/").json()

    if filtro == "Todos":
        filtrados = equipos
    elif filtro == "Estado":
        estado = st.radio("Estado:", ["Operativos", "En avería"])
        endpoint = "/equipos/operativos" if estado == "Operativos" else "/equipos/en_averia"
        filtrados = requests.get(f"{API_URL}{endpoint}").json()
    elif filtro == "Prioridad":
        nivel = st.selectbox("Nivel:", ["Alta", "Media", "Baja"])
        filtrados = requests.get(f"{API_URL}/equipos/por_prioridad/{nivel}").json()
    elif filtro == "Frecuencia":
        frec = st.selectbox("Frecuencia:", ["Mensual", "Trimestral", "Semestral", "Anual"])
        filtrados = requests.get(f"{API_URL}/equipos/por_frecuencia/{frec}").json()
    elif filtro == "Ubicación":
        ubic = st.selectbox("Ubicación:", AREAS_EQUIPO)
        filtrados = [e for e in equipos if e["ubicacion"] == ubic]

    for e in filtrados:
        st.markdown(f"- **{e['nombre']}** | 🏷 {e['ubicacion']} | ⚙ {e['prioridad_mtto']} | ⏱ {e['frecuencia_mtto']}")

# ------------------------------
# ℹ️ VER DETALLES
# ------------------------------
elif menu == "ℹ️ Ver detalles de equipo":
    st.header("ℹ️ Detalles del equipo")
    equipos = requests.get(f"{API_URL}/indicadores/equipos/resumen").json()
    opciones = {f"{e['nombre']} - ID {e['id']}": e["id"] for e in equipos}
    seleccionado = st.selectbox("Selecciona equipo", opciones.keys())

    if seleccionado:
        id = opciones[seleccionado]
        d = requests.get(f"{API_URL}/indicadores/equipos/{id}/detalles").json()
        st.write(f"**Nombre:** {d['nombre']}")
        st.write(f"**Marca:** {d['marca']}")
        st.write(f"**Modelo:** {d['modelo']}")
        st.write(f"**Serie:** {d['serie']}")
        st.write(f"**Ubicación:** {d['ubicacion']}")
        st.write(f"**Fecha adquisición:** {d['fecha_adquisicion']}")
        st.write(f"**Estado:** {'✅ Operativo' if d['estado_operativo'] else '❌ En avería'}")
        st.write(f"**Tipo:** {d['tipo']}")
        st.write(f"**Prioridad:** {d['prioridad']}")
        st.write(f"**Frecuencia:** {d['frecuencia_mantenimiento']}")
        st.write(f"**Proveedor:** {d['proveedor']}")
        st.write(f"**Contrato:** {d['contrato']}")

elif menu == "📥 Exportar a Excel":
    st.header("📥 Exportar equipos a Excel")

    equipos = requests.get(f"{API_URL}/equipos/").json()
    if not equipos:
        st.warning("No hay datos para exportar.")
    else:
        df = pd.DataFrame(equipos)

        # Opcional: selecciona columnas
        columnas = st.multiselect("Selecciona columnas a exportar", df.columns.tolist(), default=df.columns.tolist())

        df_export = df[columnas]

        # Descargar como archivo Excel
        def to_excel(df):
            from io import BytesIO
            import xlsxwriter

            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Equipos')
            processed_data = output.getvalue()
            return processed_data

        excel_data = to_excel(df_export)

        st.download_button(
            label="📥 Descargar Excel",
            data=excel_data,
            file_name="equipos_medicos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

elif menu == "👥 Ver y eliminar usuarios":
    st.header("👥 Lista de usuarios registrados")

    usuarios = requests.get(f"{API_URL}/usuarios/").json()

    if not usuarios:
        st.info("No hay usuarios registrados.")
    else:
        df_usuarios = pd.DataFrame(usuarios)
        st.dataframe(df_usuarios.drop(columns=["contraseña_encriptada"]), use_container_width=True)

        st.subheader("🗑️ Eliminar usuario")

        opciones = {f"{u['nombre']} ({u['correo']}) - ID {u['id']}": u["id"] for u in usuarios}
        seleccionado = st.selectbox("Selecciona un usuario", opciones.keys())

        if seleccionado:
            user_id = opciones[seleccionado]
            user_data = [u for u in usuarios if u["id"] == user_id][0]

            st.write(f"**Nombre:** {user_data['nombre']}")
            st.write(f"**Correo:** {user_data['correo']}")
            st.write(f"**Rol:** {user_data['rol']}")
            st.warning("⚠️ Esta acción eliminará permanentemente al usuario.")

            if st.button("Eliminar usuario permanentemente"):
                r = requests.delete(f"{API_URL}/usuarios/{user_id}")
                if r.status_code == 200:
                    st.success("✅ Usuario eliminado correctamente")
                    st.stop()
                else:
                    st.error("❌ Error al eliminar usuario")
                    st.json(r.json())

elif menu == "📝 Registrar mantenimiento":
    st.header("📝 Registrar mantenimiento de equipo")

    equipos = requests.get(f"{API_URL}/equipos/").json()
    if equipos:
        opciones = {f"{e['nombre']} - ID {e['id']}": e["id"] for e in equipos}
        seleccionado = st.selectbox("Selecciona un equipo", opciones.keys())
        if seleccionado:
            equipo_id = opciones[seleccionado]

            with st.form("form_mantenimiento"):
                tipo = st.selectbox("Tipo de mantenimiento", ["Preventivo", "Correctivo"])
                fecha_programada = st.date_input("Fecha programada")
                tecnico = st.text_input("Nombre del técnico")
                observaciones = st.text_area("Observaciones")
                enviar = st.form_submit_button("Guardar mantenimiento")

                if enviar:
                    data = {
                        "id_equipo": equipo_id,
                        "tipo": tipo,
                        "fecha_programada": f"{fecha_programada}T00:00:00",
                        "tecnico": tecnico,
                        "observaciones": observaciones
                    }
                    r = requests.post(f"{API_URL}/mantenimientos/", json=data)
                    if r.status_code == 200:
                        st.success("✅ Mantenimiento registrado")
                    else:
                        st.error("❌ Error al guardar mantenimiento")
                        st.json(r.json())

elif menu == "🛠️ Mantenimientos":
    st.header("🛠️ Mantenimientos programados y realizados")

    opcion = st.radio("¿Qué deseas ver?", ["Por equipo", "Próximos mantenimientos"])

    if opcion == "Por equipo":
        equipos = requests.get(f"{API_URL}/equipos/").json()
        if equipos:
            opciones = {f"{e['nombre']} - ID {e['id']}": e["id"] for e in equipos}
            seleccionado = st.selectbox("Selecciona un equipo", opciones.keys())

            if seleccionado:
                equipo_id = opciones[seleccionado]
                mantenimientos = requests.get(f"{API_URL}/mantenimientos/equipo/{equipo_id}").json()

                if not mantenimientos:
                    st.info("Este equipo no tiene mantenimientos registrados.")
                else:
                    if isinstance(mantenimientos, dict):
                        mantenimientos = [mantenimientos]
                    df = pd.DataFrame(mantenimientos)
                    st.dataframe(df, use_container_width=True)
        else:
            st.warning("No hay equipos registrados.")

    elif opcion == "Próximos mantenimientos":
        todos = requests.get(f"{API_URL}/mantenimientos/").json()
        if not todos:
            st.info("No hay mantenimientos registrados.")
        else:
            df = pd.DataFrame(todos)
            hoy = pd.to_datetime("today")
            df["fecha_programada"] = pd.to_datetime(df["fecha_programada"])
            proximos = df[df["fecha_programada"] >= hoy].sort_values("fecha_programada")

            st.dataframe(proximos, use_container_width=True)

elif menu == "🔎 Ver mantenimientos por equipo":
    st.header("🔎 Mantenimientos por equipo")

    equipos = requests.get(f"{API_URL}/equipos/").json()
    if equipos:
        opciones = {f"{e['nombre']} - ID {e['id']}": e["id"] for e in equipos}
        seleccionado = st.selectbox("Selecciona un equipo", opciones.keys())

        if seleccionado:
            equipo_id = opciones[seleccionado]
            r = requests.get(f"{API_URL}/mantenimientos/equipo/{equipo_id}")

            if r.status_code == 200:
                mantenimientos = r.json()
                if mantenimientos:
                    df = pd.DataFrame(mantenimientos)
                    df = df[["tipo", "fecha_programada", "fecha_realizada", "tecnico", "observaciones"]]
                    df.columns = ["Tipo", "Fecha Programada", "Fecha Realizada", "Técnico", "Observaciones"]
                    st.dataframe(df, use_container_width=True)
                else:
                    st.info("⚠️ Este equipo aún no tiene mantenimientos registrados.")
            else:
                st.warning("⚠️ Este equipo aún no tiene mantenimientos registrados.")

elif menu == "📝 Marcar mantenimiento como realizado":
    st.header("📝 Marcar mantenimiento como realizado")

    try:
        mantenimientos = requests.get(f"{API_URL}/mantenimientos/").json()
        pendientes = [m for m in mantenimientos if m["fecha_realizada"] is None]
    except:
        pendientes = []
        st.error("❌ No se pudo cargar la lista de mantenimientos.")

    if pendientes:
        opciones = {f"{m['tipo']} - Equipo {m['id_equipo']} - ID {m['id']}": m["id"] for m in pendientes}
        seleccion = st.selectbox("Selecciona un mantenimiento pendiente", opciones.keys())

        with st.form("form_marcar_realizado"):
            fecha = st.date_input("📅 Fecha de realización")
            archivo = st.file_uploader("📎 Subir hoja de servicio (PDF)", type=["pdf"])
            enviar = st.form_submit_button("✅ Confirmar")

        if enviar:
            if not archivo:
                st.warning("⚠️ Debes subir la hoja de servicio.")
            else:
                id_mantenimiento = opciones[seleccion]
                
                # 1. Marcar como realizado (fecha)
                r1 = requests.put(
                    f"{API_URL}/mantenimientos/realizar/{id_mantenimiento}",
                    data=f'"{fecha}T00:00:00"',
                    headers={"Content-Type": "application/json"}
                )

                # 2. Subir hoja PDF
                r2 = requests.post(
                    f"{API_URL}/archivos/subir_hoja/{id_mantenimiento}",
                    files={"file": archivo}
                )

                if r1.status_code == 200 and r2.status_code == 200:
                    st.success("✅ Mantenimiento marcado y hoja guardada.")
                    st.rerun()
                else:
                    st.error("❌ Error al guardar los datos.")
                    st.write("Mantenimiento:", r1.text)
                    st.write("Archivo:", r2.text)
    else:
        st.info("🎉 No hay mantenimientos pendientes.")

elif menu == "📅 Próximos mantenimientos":
    st.header("📅 Mantenimientos próximos")
    import xlsxwriter
    import io

    dias = st.slider("Mostrar próximos mantenimientos en los próximos días:", 1, 30, 15)
    r = requests.get(f"{API_URL}/mantenimientos/proximos/?dias={dias}")
    mantenimientos = requests.get(f"{API_URL}/mantenimientos/").json()
    proximos = [m for m in mantenimientos if m["fecha_programada"] and ... ]
    df_proximos = pd.DataFrame(proximos)
    
    if not df_proximos.empty:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_proximos.to_excel(writer, index=False, sheet_name='Proximos')
            
        output.seek(0)
        
        st.download_button(
        label="📥 Descargar Excel de próximos mantenimientos",
        data=output,
        file_name="proximos_mantenimientos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    if r.status_code == 200:
        mantenimientos = r.json()
        if not mantenimientos:
            st.success("✅ No hay mantenimientos pendientes en este rango de fechas.")
        else:
            df = pd.DataFrame(mantenimientos)
            df["fecha_programada"] = pd.to_datetime(df["fecha_programada"]).dt.date
            df["fecha_realizada"] = pd.to_datetime(df["fecha_realizada"]).dt.date
            df["estado"] = df["fecha_realizada"].apply(lambda x: "✅ Realizado" if pd.notnull(x) else "⏳ Pendiente")

            equipos_dict = {e["id"]: e["nombre"] for e in requests.get(f"{API_URL}/equipos/").json()}
            df["equipo"] = df["id_equipo"].map(equipos_dict)

            columnas = ["equipo", "tipo", "fecha_programada", "estado", "tecnico", "observaciones"]
            df = df[columnas]
            df.columns = ["Equipo", "Tipo", "Fecha Programada", "Estado", "Técnico", "Observaciones"]

            st.dataframe(df, use_container_width=True)

            
    else:
        st.error("⚠️ No se pudo obtener la información del backend.")