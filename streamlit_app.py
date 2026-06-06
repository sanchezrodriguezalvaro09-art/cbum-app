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
conn = sqlite3.connect('fitness_elite_v9.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (nombre TEXT PRIMARY KEY, password TEXT, objetivo TEXT, dias INTEGER)''')
conn.commit()

if 'user' not in st.session_state: st.session_state.user = None
if 'page' not in st.session_state: st.session_state.page = "Inicio"

# --- Lógica de IA ---
def generar_rutina(obj, dias):
    rutinas = {
        "Hipertrofia": ["Pecho/Tríceps", "Espalda/Bíceps", "Pierna/Hombro", "FullBody"],
        "Fuerza": ["Empuje pesado", "Tracción pesada", "Pierna pesada", "Core/Accesorios"]
    }
    ejercicios = {
        "Pecho/Tríceps": ["Press Banca 4x10", "Aperturas 3x12", "Press Francés 3x10"],
        "Espalda/Bíceps": ["Dominadas 3xFalló", "Remo Barra 4x10", "Curl Barra 3x12"]
    }
    plan = {}
    for i in range(dias):
        musculos = rutinas.get(obj, ["Día genérico"])[i % len(rutinas.get(obj, ["Día genérico"]))]
        plan[f"Día {i+1}: {musculos}"] = ejercicios.get(musculos, ["Ejercicio IA 3x10"])
    return plan

# --- Login ---
if st.session_state.user is None:
    st.title("CBUM ELITE")
    choice = st.radio("Acceso:", ["Iniciar Sesión", "Registrarse"])
    n, p = st.text_input("Usuario"), st.text_input("Contraseña", type="password")
    if choice == "Registrarse":
        obj = st.selectbox("Objetivo", ["Hipertrofia", "Fuerza"])
        dias = st.slider("Días", 3, 5, 4)
        if st.button("Crear"):
            c.execute("INSERT INTO usuarios VALUES (?,?,?,?)", (n, p, obj, dias))
            conn.commit()
    elif st.button("Entrar"):
        c.execute("SELECT objetivo, dias FROM usuarios WHERE nombre=? AND password=?", (n, p))
        res = c.fetchone()
        if res:
            st.session_state.user = n
            st.session_state.obj, st.session_state.dias = res
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

    # Vistas
    if st.session_state.page == "Inicio":
        st.title(f"Bienvenido, {st.session_state.user}")
    
    elif st.session_state.page == "Entrenar":
        st.subheader("Rutina Semanal Completa")
        plan = generar_rutina(st.session_state.obj, st.session_state.dias)
        for dia, ejer in plan.items():
            with st.expander(dia):
                for e in ejer: st.write(f"- {e}")

    elif st.session_state.page == "Supl":
        st.subheader("Suplementación")
        st.write("Proteína y Creatina según tu objetivo.")

    elif st.session_state.page == "Progreso":
        st.subheader("Seguimiento")
        st.write("Gráficos y pesos.")

