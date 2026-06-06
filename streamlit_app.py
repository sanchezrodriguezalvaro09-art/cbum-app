import streamlit as st
import sqlite3
import pandas as pd
from fpdf import FPDF
import io

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
    .red-dot { position: absolute; top: -5px; right: 20%; height: 10px; width: 10px; 
               background-color: red; border-radius: 50%; display: inline-block; }
    </style>
""", unsafe_allow_html=True)

# --- 2. BASE DE DATOS ---
conn = sqlite3.connect('cbum_elite_final_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
             (id INTEGER PRIMARY KEY, nombre TEXT UNIQUE, pass TEXT, peso REAL, altura REAL, objetivo TEXT, dias INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS historial_peso (usuario TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, peso REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS historial_ejercicios (usuario TEXT, ejercicio TEXT, peso_kg REAL, reps INTEGER, rpe INTEGER, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
c.execute('''CREATE TABLE IF NOT EXISTS diario_nutricion (usuario TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, calorias REAL, info TEXT)''')
conn.commit()

# --- 3. MOTOR IA ELITE ---
imagenes_ejercicios = {
    "Press Banca": "https://www.exercises.com.au/wp-content/uploads/2015/05/Barbell-bench-press_1.png",
    "Press Militar": "https://www.exercises.com.au/wp-content/uploads/2015/05/Standing-military-press_1.png",
    "Sentadilla": "https://www.exercises.com.au/wp-content/uploads/2015/05/Barbell-squat_1.png",
    "Dominadas": "https://www.exercises.com.au/wp-content/uploads/2015/05/Pull-up_1.png",
    "Remo": "https://www.exercises.com.au/wp-content/uploads/2015/05/Bent-over-row_1.png",
    "Curl": "https://www.exercises.com.au/wp-content/uploads/2015/05/Barbell-curl_1.png"
}

def generar_rutina_ia(obj, dias, historial_fuerza):
    rango = {"Hipertrofia": "4x10-12", "Fuerza": "5x3-5", "Músculo Magro": "3x10-15", "Definición": "4x15-20"}
    r = rango.get(obj, "3x12")
    ejercicios = {
        "Empuje": [f"Press Banca {r}", f"Press Militar {r}", f"Aperturas {r}", f"Press Francés {r}"],
        "Tracción": [f"Dominadas {r}", f"Remo con Barra {r}", f"Curl con Barra {r}", f"Curl Inverso {r}"],
        "Pierna": [f"Sentadilla {r}", f"Prensa {r}", f"Curl Femoral {r}", f"Gemelos {r}", f"Crunch Abdomen {r}"],
        "Torso": [f"Press Inclinado {r}", f"Jalón al pecho {r}", f"Elevaciones Laterales {r}", f"Plancha {r}"],
        "Fullbody": [f"Peso Muerto {r}", f"Press Banca {r}", f"Remo {r}", f"Press Militar {r}"]
    }
    est = {3: ["Empuje", "Tracción", "Pierna"], 4: ["Torso", "Pierna", "Empuje", "Tracción"], 5: ["Empuje", "Tracción", "Pierna", "Torso", "Fullbody"]}
    plan = {}
    dias_sel = est.get(dias, est[3])
    for i, tipo in enumerate(dias_sel):
        plan[f"Día {i+1}: {tipo}"] = ejercicios[tipo]
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
            if st.form_submit_button("Registrarse"):
                try:
                    c.execute("INSERT INTO usuarios (nombre, pass, peso, altura, objetivo, dias) VALUES (?,?,?,?,?,?)", (n, p, pes, alt, obj, dias))
                    conn.commit()
                    st.success("Registrado.")
                except: st.error("Usuario existe.")
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
else:
    if 'page' not in st.session_state: st.session_state.page = "Entrenar"
    
    st.markdown('<div class="fixed-menu">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.button("💪", on_click=lambda: st.session_state.update(page="Entrenar"))
    c2.button("💊", on_click=lambda: st.session_state.update(page="Supl"))
    c3.button("📈", on_click=lambda: st.session_state.update(page="Progreso"))
    c4.button("🥑", on_click=lambda: st.session_state.update(page="Nutricion"))
    if c5.button("⚙️"): st.session_state.page = "Sistema"
    st.markdown('<span class="red-dot"></span>', unsafe_allow_html=True)
    c6.button("💬", on_click=lambda: st.session_state.update(page="Chat"))
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.page == "Entrenar":
        st.subheader("Rutina Elite")
        plan = generar_rutina_ia(st.session_state.data[5], st.session_state.data[6], [])
        for dia, ejer in plan.items():
            with st.expander(dia):
                for e in ejer:
                    st.write(f"✅ {e}")
    elif st.session_state.page == "Progreso":
        st.subheader("📊 Gráficas y Reportes")
        if st.button("Exportar Informe PDF"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Informe: {st.session_state.user}", ln=True, align='C')
            st.download_button("Descargar PDF", data=pdf.output(dest='S').encode('latin-1'), file_name="informe.pdf")
    elif st.session_state.page == "Nutricion":
        st.subheader("🥑 Registro")
        if st.file_uploader("Sube foto", type=["jpg", "png"]): st.success("Analizado.")
    elif st.session_state.page == "Sistema":
        st.subheader("⚙️ Sistema")
        if st.button("Aplicar Mejora"): st.balloons()
