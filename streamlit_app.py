import streamlit as st
import sqlite3

# --- 1. CONFIGURACIÓN ELITE ---
st.set_page_config(page_title="CBum Elite Pro", layout="centered")
st.markdown("""
    <style>
    .stApp { background: #000000; color: #FFD700; }
    .fixed-menu { position: fixed; bottom: 0; left: 0; width: 100%; background: #0a0a0a; 
                  padding: 15px; display: flex; justify-content: space-around; 
                  border-top: 2px solid #0000FF; z-index: 999; }
    .stButton button { color: #FFD700; background-color: #111; border: 1px solid #0000FF; width: 100%; }
    h1, h2 { color: #FFD700 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. BASE DE DATOS (v14) ---
conn = sqlite3.connect('cbum_elite_v14.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
             (id INTEGER PRIMARY KEY, nombre TEXT UNIQUE, pass TEXT, peso REAL, altura REAL, objetivo TEXT, dias INTEGER)''')
conn.commit()

# --- 3. GESTIÓN DE SESIÓN ---
if 'user' not in st.session_state: st.session_state.user = None
if 'data' not in st.session_state: st.session_state.data = None

# --- 4. PANTALLA DE ACCESO ---
if not st.session_state.user:
    st.title("🚀 CBUM ELITE PRO")
    tab1, tab2 = st.tabs(["ENTRAR", "REGISTRO ELITE"])
    
    with tab2: # REGISTRO
        n = st.text_input("Nombre de Usuario", key="reg_n")
        p = st.text_input("Contraseña", type="password", key="reg_p")
        alt = st.number_input("Altura (cm)", 150, 220, 180)
        pes = st.number_input("Peso (kg)", 50.0, 150.0, 80.0)
        obj = st.selectbox("Objetivo", ["Hipertrofia", "Fuerza"])
        dias = st.slider("Días de entreno", 3, 5, 4)
        if st.button("Registrarse"):
            try:
                c.execute("INSERT INTO usuarios (nombre, pass, peso, altura, objetivo, dias) VALUES (?,?,?,?,?,?)", (n, p, pes, alt, obj, dias))
                conn.commit()
                st.success("Usuario creado. Ve a la pestaña 'ENTRAR'.")
            except: st.error("Ese usuario ya existe.")

    with tab1: # LOGIN
        un = st.text_input("User", key="log_n")
        up = st.text_input("Pass", type="password", key="log_p")
        if st.button("Acceder"):
            c.execute("SELECT * FROM usuarios WHERE nombre=? AND pass=?", (un, up))
            user = c.fetchone()
            if user:
                st.session_state.user = user[1]
                st.session_state.data = user
                st.rerun() # ESTO FORZA A QUE LA APP SE RECARGUE EN MODO LOGUEADO
            else: st.error("Usuario o contraseña incorrectos.")

# --- 5. APP PRINCIPAL (ELITE) ---
else:
    # MENÚ FIJO INFERIOR
    st.markdown('<div class="fixed-menu">', unsafe_allow_html=True)
    cols = st.columns(4)
    if cols[0].button("💪"): st.session_state.page = "Entrenar"
    if cols[1].button("💊"): st.session_state.page = "Supl"
    if cols[2].button("📈"): st.session_state.page = "Progreso"
    if cols[3].button("💬"): st.session_state.page = "Chat"
    st.markdown('</div>', unsafe_allow_html=True)

    # Lógica de pantallas
    page = st.session_state.get("page", "Entrenar")
    if page == "Entrenar":
        st.subheader("Rutina de Élite")
        st.write(f"Bienvenido {st.session_state.user}. Tu plan para {st.session_state.data[5]} está listo.")
    elif page == "Supl":
        st.subheader("Suplementación")
    elif page == "Progreso":
        st.subheader("Seguimiento de Progreso")
        st.write(f"Peso inicial: {st.session_state.data[3]} kg")
    elif page == "Chat":
        st.subheader("Asistente IA")

