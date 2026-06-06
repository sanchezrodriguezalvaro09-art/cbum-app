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
conn = sqlite3.connect('cbum_elite_full.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
             (id INTEGER PRIMARY KEY, nombre TEXT UNIQUE, pass TEXT, peso REAL, altura REAL, objetivo TEXT, dias INTEGER)''')
conn.commit()

# --- 3. MOTOR DE IA PARA RUTINAS ---
def generar_rutina_ia(obj, dias):
    # Base de ejercicios completa
    ejercicios_base = {
        "Pecho": ["Press Banca", "Aperturas con mancuernas", "Press Inclinado"],
        "Espalda": ["Dominadas", "Remo con barra", "Jalón al pecho"],
        "Hombro": ["Press Militar", "Elevaciones laterales", "Pájaros"],
        "Piernas": ["Sentadilla", "Prensa", "Extensiones", "Curl Femoral"],
        "Brazos": ["Curl Barra", "Press Francés", "Antebrazo con barra"],
        "Abdomen": ["Plancha", "Crunch", "Elevación de piernas"]
    }
    
    # IA reparte grupos musculares según los días elegidos
    plan = {}
    grupos = list(ejercicios_base.keys())
    for i in range(dias):
        # Distribución inteligente: 2 grupos por día
        g1 = grupos[i % len(grupos)]
        g2 = grupos[(i + 1) % len(grupos)]
        plan[f"Día {i+1}: {g1} + {g2}"] = ejercicios_base[g1] + ejercicios_base[g2]
    return plan

# --- 4. GESTIÓN SESIÓN ---
if 'user' not in st.session_state: st.session_state.user = None

if not st.session_state.user:
    st.title("🚀 CBUM ELITE PRO")
    tab1, tab2 = st.tabs(["ENTRAR", "REGISTRO ELITE"])
    with tab2:
        with st.form("reg"):
            n, p = st.text_input("Usuario"), st.text_input("Contraseña", type="password")
            alt, pes = st.number_input("Altura"), st.number_input("Peso")
            obj = st.selectbox("Objetivo", ["Hipertrofia", "Fuerza", "Músculo Magro", "Definición"])
            dias = st.slider("Días", 3, 5, 4)
            if st.form_submit_button("Registrar"):
                try:
                    c.execute("INSERT INTO usuarios (nombre, pass, peso, altura, objetivo, dias) VALUES (?,?,?,?,?,?)", (n, p, pes, alt, obj, dias))
                    conn.commit()
                    st.success("Registrado.")
                except: st.error("Error.")
    with tab1:
        with st.form("login"):
            un, up = st.text_input("User"), st.text_input("Pass", type="password")
            if st.form_submit_button("Acceder"):
                c.execute("SELECT * FROM usuarios WHERE nombre=? AND pass=?", (un, up))
                user = c.fetchone()
                if user:
                    st.session_state.user = user[1]
                    st.session_state.data = user
                    st.rerun()

# --- 5. APP PRINCIPAL ---
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

    if st.session_state.page == "Entrenar":
        st.subheader("Rutina IA Completa")
        plan = generar_rutina_ia(st.session_state.data[5], st.session_state.data[6])
        for dia, ejer in plan.items():
            with st.expander(dia):
                for e in ejer: st.write(f"✅ {e} - 3 series x 12 reps")
    
    elif st.session_state.page == "Chat":
        st.subheader("IA Coach")
        query = st.text_input("Pregunta a tu entrenador IA:")
        if query: st.write("IA: Basado en tus datos, ajusta el peso si la última serie es fácil.")

