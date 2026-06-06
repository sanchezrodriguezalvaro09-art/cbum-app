import streamlit as st
import sqlite3

# Configuración visual
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

# Base de datos
conn = sqlite3.connect('fitness_elite_v11.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (nombre TEXT PRIMARY KEY, password TEXT, altura REAL, peso REAL, objetivo TEXT, dias INTEGER)''')
conn.commit()

# --- IA: Generador de Plan Completo ---
def get_plan(obj):
    # Diccionario con rutinas variadas para trabajar todo el cuerpo
    planes = {
        "Hipertrofia": {
            "Día 1: Pecho/Tríceps": [("Press Banca Plano", "https://via.placeholder.com/150"), ("Press Francés", "https://via.placeholder.com/150")],
            "Día 2: Espalda/Bíceps": [("Remo con Barra", "https://via.placeholder.com/150"), ("Curl de Bíceps", "https://via.placeholder.com/150")],
            "Día 3: Pierna": [("Sentadilla Libre", "https://via.placeholder.com/150"), ("Prensa", "https://via.placeholder.com/150")]
        }
    }
    return planes.get(obj, {"Día 1": [("Ejercicio Base", "https://via.placeholder.com/150")]})

# --- Sesión ---
if 'user' not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    st.title("CBUM ELITE")
    n, p = st.text_input("Usuario"), st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        c.execute("SELECT objetivo, dias, altura, peso FROM usuarios WHERE nombre=? AND password=?", (n, p))
        res = c.fetchone()
        if res:
            st.session_state.user = n
            st.session_state.obj, st.session_state.dias, st.session_state.alt, st.session_state.peso = res
            st.rerun()
else:
    # Menú inferior
    st.markdown('<div class="fixed-menu">', unsafe_allow_html=True)
    cols = st.columns(4)
    if cols[0].button("💪"): st.session_state.page = "Entrenar"
    if cols[1].button("💊"): st.session_state.page = "Supl"
    if cols[2].button("📈"): st.session_state.page = "Progreso"
    if cols[3].button("💬"): st.session_state.page = "Chat"
    st.markdown('</div>', unsafe_allow_html=True)

    # Vista Entrenar con IA detallada
    if st.session_state.page == "Entrenar":
        st.subheader("Tu Rutina Personalizada")
        plan = get_plan(st.session_state.obj)
        for dia, ejercicios in plan.items():
            with st.expander(dia):
                for nombre, img in ejercicios:
                    st.write(f"### {nombre}")
                    st.image(img, caption=nombre)
                    st.write("Series: 4 | Repeticiones: 10-12")

