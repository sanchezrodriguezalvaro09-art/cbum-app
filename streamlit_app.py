import streamlit as st
import sqlite3
import time

# --- Configuración inicial ---
st.set_page_config(page_title="CBum Elite Training", layout="centered")

# --- Base de datos (Persistencia de datos) ---
conn = sqlite3.connect('fitness_data.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS pesos (usuario TEXT, fecha TEXT, ejercicio TEXT, peso REAL)''')
conn.commit()

# --- CSS Estilo ---
st.markdown("""
    <style>
    .timer-box { font-size: 80px; text-align: center; color: #FF0000; font-weight: bold; background: #000; padding: 50px; border-radius: 20px; }
    h1 { color: #FFD700; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# --- Gestión de Sesión ---
if 'usuario' not in st.session_state: st.session_state.usuario = None

if st.session_state.usuario is None:
    st.title("CBUM ELITE TRAINING")
    nombre = st.text_input("Nombre de usuario")
    if st.button("Iniciar Sesión"):
        if nombre:
            st.session_state.usuario = nombre
            st.rerun()
else:
    st.title(f"Bienvenido, {st.session_state.usuario} 👋")
    
    # --- Navegación ---
    menu = st.radio("Menú", ["Entrenamiento", "Suplementación", "Progreso", "Ajustes"], horizontal=True)
    st.markdown("---")
    
    if menu == "Entrenamiento":
        equipo = st.selectbox("Estilo de entrenamiento:", ["Mancuernas", "Máquinas", "Fusionado (Híbrido)", "Peso Libre"])
        
        # --- Temporizador de Bloqueo ---
        if 'iniciar_timer' not in st.session_state: st.session_state.iniciar_timer = False
        
        if st.button("⏱️ Iniciar descanso (90s)"):
            st.session_state.iniciar_timer = True
            
        if st.session_state.iniciar_timer:
            placeholder = st.empty()
            for s in range(90, 0, -1):
                placeholder.markdown(f"<div class='timer-box'>⏳ {s}s</div>", unsafe_allow_html=True)
                time.sleep(1)
            st.session_state.iniciar_timer = False
            st.rerun()
            
        # --- Rutina (Visible si no hay timer) ---
        else:
            st.subheader(f"Rutina: {equipo}")
            ejercicio_ejemplo = "Press Inclinado"
            peso_registro = st.number_input(f"Peso para {ejercicio_ejemplo} (kg)", min_value=0.0, step=0.5)
            if st.button("Guardar Peso"):
                c.execute("INSERT INTO pesos VALUES (?, ?, ?, ?)", (st.session_state.usuario, time.strftime("%Y-%m-%d"), ejercicio_ejemplo, peso_registro))
                conn.commit()
                st.success("¡Peso guardado correctamente!")

    elif menu == "Suplementación":
        st.subheader("💊 Protocolo de Suplementación")
        st.write("Recordatorio: Toma tu proteína y creatina post-entreno.")
        notif = st.toggle("Activar notificaciones en móvil")
        if notif:
            st.info("✅ Permiso concedido. Avisos de suplementación activos.")

    elif menu == "Progreso":
        st.subheader("📈 Tu Evolución")
        st.write("Aquí verás tus marcas guardadas en la base de datos.")
        # Ejemplo de lectura de datos
        datos = c.execute("SELECT * FROM pesos WHERE usuario=?", (st.session_state.usuario,)).fetchall()
        st.table(datos)

    elif menu == "Ajustes":
        if st.button("Cerrar Sesión"):
            st.session_state.usuario = None
            st.rerun()

