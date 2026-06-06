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

# --- 2. BASE DE DATOS ---
conn = sqlite3.connect('cbum_elite_final.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
             (id INTEGER PRIMARY KEY, nombre TEXT UNIQUE, pass TEXT, peso REAL, altura REAL, objetivo TEXT, dias INTEGER)''')
conn.commit()

# --- 3. GESTIÓN DE SESIÓN ---
if 'user' not in st.session_state: st.session_state.user = None

# --- 4. LÓGICA DE LA IA ---
def get_rutina_ia(obj):
    planes = {
        "Hipertrofia": {"Día 1: Pecho/Tríceps": ["Press Banca 4x10", "Press Militar 3x10"]},
        "Fuerza": {"Día 1: Básico Pesado": ["Sentadilla 5x5", "Peso Muerto 5x5"]},
        "Músculo Magro": {"Día 1: Torso": ["Press Inclinado 3x12", "Jalón Pecho 3x12"]},
        "Definición": {"Día 1: HIIT": ["Burpees 4x45seg", "Sprints 10x30seg"]}
    }
    return planes.get(obj, {"Día 1: General": ["Rutina adaptada"]})

# --- 5. PANTALLA DE ACCESO ---
if not st.session_state.user:
    st.title("🚀 CBUM ELITE PRO")
    tab1, tab2 = st.tabs(["ENTRAR", "REGISTRO ELITE"])
    
    with tab2: # REGISTRO
        with st.form("reg_form"):
            n = st.text_input("Nombre de Usuario")
            p = st.text_input("Contraseña", type="password")
            alt = st.number_input("Altura (cm)", 150, 220, 180)
            pes = st.number_input("Peso (kg)", 50.0, 150.0, 80.0)
            obj = st.selectbox("Objetivo", ["Hipertrofia", "Fuerza", "Músculo Magro", "Definición"])
            dias = st.slider("Días de entreno", 3, 5, 4)
            if st.form_submit_button("Registrarse"):
                try:
                    c.execute("INSERT INTO usuarios (nombre, pass, peso, altura, objetivo, dias) VALUES (?,?,?,?,?,?)", (n, p, pes, alt, obj, dias))
                    conn.commit()
                    st.success("Registrado. ¡Ya puedes entrar!")
                except: st.error("Error: El usuario ya existe.")
            
    with tab1: # LOGIN
        with st.form("login_form"):
            un = st.text_input("Usuario")
            up = st.text_input("Contraseña", type="password")
            if st.form_submit_button("Acceder"):
                c.execute("SELECT * FROM usuarios WHERE nombre=? AND pass=?", (un, up))
                user = c.fetchone()
                if user:
                    st.session_state.user = user[1]
                    st.session_state.data = user
                    st.rerun()
                else: st.error("Credenciales incorrectas.")

# --- 6. APP PRINCIPAL ---
else:
    if 'page' not in st.session_state: st.session_state.page = "Entrenar"
    
    # MENÚ FIJO
    st.markdown('<div class="fixed-menu">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("💪"): st.session_state.page = "Entrenar"
    if c2.button("💊"): st.session_state.page = "Supl"
    if c3.button("📈"): st.session_state.page = "Progreso"
    if c4.button("💬"): st.session_state.page = "Chat"
    st.markdown('</div>', unsafe_allow_html=True)

    # VISTAS
    if st.session_state.page == "Entrenar":
        st.subheader(f"Objetivo: {st.session_state.data[5]}")
        rutina = get_rutina_ia(st.session_state.data[5])
        for dia, ejer in rutina.items():
            with st.expander(dia):
                for e in ejer: st.write(f"✅ {e}")
    elif st.session_state.page == "Supl":
        st.subheader("Suplementación Elite")
    elif st.session_state.page == "Progreso":
        st.subheader(f"Seguimiento: {st.session_state.data[3]} kg")
    elif st.session_state.page == "Chat":
        st.subheader("Asistente IA")

