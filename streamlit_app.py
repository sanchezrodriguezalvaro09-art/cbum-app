import streamlit as st
import sqlite3
import datetime

# --- Configuración Visual (Estilo Elite) ---
st.set_page_config(page_title="CBum Elite Training", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFD700; }
    h1, h2, h3 { color: #FFD700 !important; }
    /* Fondo con gradiente azul para simular rayos */
    .stApp { background: linear-gradient(135deg, #000000 30%, #0000FF 100%); }
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
conn = sqlite3.connect('fitness_elite_v6.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (nombre TEXT PRIMARY KEY, password TEXT, objetivo TEXT)''')
conn.commit()

# --- Gestión de Estado ---
if 'user' not in st.session_state: st.session_state.user = None
if 'page' not in st.session_state: st.session_state.page = "Inicio"

# --- LOGIN / REGISTRO ---
if st.session_state.user is None:
    st.title("CBUM ELITE TRAINING")
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    with tab2:
        n = st.text_input("Usuario", key="rn")
        p = st.text_input("Contraseña", type="password", key="rp")
        obj = st.selectbox("Objetivo", ["Hipertrofia", "Fuerza", "Músculo Magro", "Definición"])
        if st.button("Registrarse"):
            c.execute("INSERT INTO usuarios VALUES (?,?,?)", (n, p, obj))
            conn.commit()
            st.success("Registrado.")
    with tab1:
        u = st.text_input("Usuario", key="un")
        pw = st.text_input("Contraseña", type="password", key="up")
        if st.button("Entrar"):
            c.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?", (u, pw))
            if c.fetchone():
                st.session_state.user = u
                st.session_state.page = "Inicio"
                st.rerun()
else:
    # --- Bienvenida Inicial ---
    if st.session_state.page == "Inicio":
        st.title(f"Bienvenido, {st.session_state.user}")
        st.write("Selecciona una opción en el menú inferior para comenzar.")

    # --- MENÚ FIJO INFERIOR ---
    st.markdown('<div class="fixed-menu">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("💪"): st.session_state.page = "Entrenar"
    if c2.button("💊"): st.session_state.page = "Supl"
    if c3.button("📈"): st.session_state.page = "Progreso"
    if c4.button("💬"): st.session_state.page = "Chat"
    st.markdown('</div>', unsafe_allow_html=True)

    # --- LÓGICA DE NAVEGACIÓN ---
    obj = c.execute("SELECT objetivo FROM usuarios WHERE nombre=?", (st.session_state.user,)).fetchone()[0]

    if st.session_state.page == "Entrenar":
        st.subheader("Tu Rutina de Entrenamiento")
        st.write(f"Objetivo actual: {obj}")
        st.write("Generando rutina basada en tu objetivo...")
        # Aquí puedes expandir la lógica según el objetivo seleccionado

    elif st.session_state.page == "Supl":
        st.subheader("Suplementación Elite")
        st.write("Dosis recomendadas según tu perfil.")

    elif st.session_state.page == "Progreso":
        st.subheader("Control de Evolución")
        st.write("Registra tus pesos semanales aquí.")

    elif st.session_state.page == "Chat":
        st.subheader("Asistente IA")
        st.text_input("¿En qué puedo ayudarte?")

