import streamlit as st
import sqlite3
import time

# --- Configuración inicial ---
st.set_page_config(page_title="CBum Elite Training", layout="centered")

# --- Base de datos ---
conn = sqlite3.connect('fitness_app.db', check_same_thread=False)
c = conn.cursor()
# Tabla de usuarios
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (nombre TEXT PRIMARY KEY, password TEXT)''')
# Tabla de pesos
c.execute('''CREATE TABLE IF NOT EXISTS pesos (usuario TEXT, fecha TEXT, ejercicio TEXT, peso REAL)''')
conn.commit()

# --- Gestión de Sesión ---
if 'usuario' not in st.session_state: st.session_state.usuario = None

# --- Sistema de Login / Registro ---
if st.session_state.usuario is None:
    st.title("CBUM ELITE TRAINING")
    opcion = st.radio("Acceso:", ["Iniciar Sesión", "Registrarse"])
    
    usuario_input = st.text_input("Nombre de usuario")
    pass_input = st.text_input("Contraseña", type="password")
    
    if opcion == "Registrarse":
        if st.button("Crear cuenta"):
            try:
                c.execute("INSERT INTO usuarios VALUES (?, ?)", (usuario_input, pass_input))
                conn.commit()
                st.success("Cuenta creada. Ya puedes iniciar sesión.")
            except:
                st.error("El usuario ya existe.")
    else:
        if st.button("Entrar"):
            c.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?", (usuario_input, pass_input))
            if c.fetchone():
                st.session_state.usuario = usuario_input
                st.rerun()
            else:
                st.error("Usuario o contraseña incorrectos.")

# --- Aplicación (Si está logueado) ---
else:
    st.title(f"Bienvenido, {st.session_state.usuario} 👋")
    
    menu = st.radio("Menú", ["Entrenamiento", "Suplementación", "Progreso", "Ajustes"], horizontal=True)
    st.markdown("---")
    
    if menu == "Entrenamiento":
        # ... (Tu código de rutina y temporizador aquí) ...
        if st.button("⏱️ Iniciar descanso (90s)"):
            placeholder = st.empty()
            for s in range(90, 0, -1):
                placeholder.markdown(f"<h1 style='color:red;'>⏳ {s}s</h1>", unsafe_allow_html=True)
                time.sleep(1)
            st.rerun()

    elif menu == "Suplementación":
        st.subheader("💊 Protocolo")
        if st.toggle("Activar recordatorios"):
            st.info("Recordatorios activados.")

    elif menu == "Progreso":
        st.subheader("📈 Tu Evolución")
        datos = c.execute("SELECT * FROM pesos WHERE usuario=?", (st.session_state.usuario,)).fetchall()
        st.table(datos)

    elif menu == "Ajustes":
        if st.button("Cerrar Sesión"):
            st.session_state.usuario = None
            st.rerun()

