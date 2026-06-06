import streamlit as st
import sqlite3

# --- Configuración Visual ---
st.set_page_config(page_title="CBum Elite", layout="centered")
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #000000 30%, #000033 100%); color: #FFD700; }
    h1, h2, h3 { color: #FFD700 !important; }
    .fixed-menu { 
        position: fixed; bottom: 0; left: 0; width: 100%; 
        background-color: #000000; padding: 15px;
        display: flex; justify-content: space-around;
        border-top: 2px solid #0000FF; z-index: 999;
    }
    .stButton button { color: #FFD700; background-color: #111; border: 1px solid #0000FF; }
    </style>
""", unsafe_allow_html=True)

# --- Base de Datos ---
conn = sqlite3.connect('fitness_elite_v7.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
             (nombre TEXT PRIMARY KEY, password TEXT, objetivo TEXT)''')
conn.commit()

# --- Gestión de Estado ---
if 'user' not in st.session_state: st.session_state.user = None
if 'page' not in st.session_state: st.session_state.page = "Inicio"

# --- LÓGICA DE LOGIN / REGISTRO ---
if st.session_state.user is None:
    st.title("CBUM ELITE TRAINING")
    choice = st.radio("Acceso:", ["Iniciar Sesión", "Registrarse"])
    
    nombre = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    
    if choice == "Registrarse":
        objetivo = st.selectbox("Objetivo", ["Hipertrofia", "Fuerza", "Músculo Magro", "Definición"])
        if st.button("Crear cuenta"):
            try:
                c.execute("INSERT INTO usuarios VALUES (?,?,?)", (nombre, password, objetivo))
                conn.commit()
                st.success("Cuenta creada. Por favor, selecciona 'Iniciar Sesión' e introduce tus datos.")
            except: st.error("El usuario ya existe.")
    else:
        if st.button("Entrar"):
            c.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?", (nombre, password))
            if c.fetchone():
                st.session_state.user = nombre
                st.rerun()
            else: st.error("Usuario o contraseña incorrectos.")

# --- APP PRINCIPAL ---
else:
    # Menú Fijo
    st.markdown('<div class="fixed-menu">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("💪"): st.session_state.page = "Entrenar"
    if c2.button("💊"): st.session_state.page = "Supl"
    if c3.button("📈"): st.session_state.page = "Progreso"
    if c4.button("💬"): st.session_state.page = "Chat"
    st.markdown('</div>', unsafe_allow_html=True)

    # Vista Bienvenida
    if st.session_state.page == "Inicio":
        st.title(f"Bienvenido, {st.session_state.user}")
        st.write("Selecciona una opción abajo.")
    
    # Secciones
    elif st.session_state.page == "Entrenar":
        st.subheader("Rutina de Entrenamiento")
        # Aquí la lógica de carga de rutina...
    elif st.session_state.page == "Supl":
        st.subheader("Suplementación")
    elif st.session_state.page == "Progreso":
        st.subheader("Tu Progreso")
    elif st.session_state.page == "Chat":
        st.subheader("Asistente IA")

