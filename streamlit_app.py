import streamlit as st
import sqlite3
import pandas as pd
from fpdf import FPDF
import io

# --- 1. CONFIGURACIÓN ELITE ---
st.set_page_config(page_title="CBum Elite Pro", layout="centered")
st.markdown("""
    <style>
    .stApp { background: #050505; color: #FFFFFF; font-family: 'Helvetica', sans-serif; }
    .stExpander { background: #121212 !important; border: 1px solid #333 !important; border-radius: 12px !important; }
    .stButton button { 
        background: linear-gradient(90deg, #0000FF, #000044); 
        color: white; 
        border: none; 
        border-radius: 8px; 
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton button:hover { transform: scale(1.05); background: #0000FF; }
    h1, h2 { color: #00D4FF !important; text-shadow: 0px 0px 10px rgba(0, 212, 255, 0.5); }
    
    /* Ejercicios opcionales en azul */
    .stCheckbox label {
        color: #00D4FF !important;
    }
    
    .fixed-menu { 
        position: fixed; 
        bottom: 0; 
        left: 0; 
        width: 100%; 
        background: #0a0a0a; 
        padding: 10px 0; 
        display: flex; 
        justify-content: space-around; 
        border-top: 2px solid #0000FF; 
        z-index: 9999;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. BASE DE DATOS ---
conn = sqlite3.connect('cbum_elite_final_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
             (id INTEGER PRIMARY KEY, nombre TEXT UNIQUE, pass TEXT, peso REAL, altura REAL, objetivo TEXT, dias INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS historial_peso (usuario TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, peso REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS historial_ejercicios_v2 (usuario TEXT, ejercicio TEXT, peso_kg REAL, reps INTEGER, rpe INTEGER, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
c.execute('''CREATE TABLE IF NOT EXISTS diario_nutricion (usuario TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, calorias REAL, info TEXT)''')
conn.commit()

# --- 3. MOTOR IA ELITE ---
def obtener_estructura_rutina(r):
    return {
        "Empuje": {"Base": [f"Press Banca {r}", f"Press Militar {r}", f"Fondos en paralelas {r}"], "Accesorios": ["Press inclinado mancuernas 3x12", "Elevaciones laterales 3x15", "Extensión tríceps cuerda 3x15", "Cruces polea 3x12", "Facepull 3x15"]},
        "Tracción": {"Base": [f"Dominadas {r}", f"Remo con barra {r}", f"Curl con barra {r}"], "Accesorios": ["Jalón al pecho agarre neutro 3x12", "Remo polea baja 3x12", "Pájaros (hombro post) 3x15", "Curl martillo 3x12", "Antebrazo 3x15"]},
        "Pierna": {"Base": [f"Sentadilla {r}", f"Prensa {r}", f"Peso Muerto Rumano {r}"], "Accesorios": ["Extensiones cuádriceps 3x15", "Curl femoral tumbado 3x15", "Gemelos de pie 4x15", "Hip thrust 3x12", "Abdominales con peso 3x15"]},
        "Torso": {"Base": [f"Press Inclinado {r}", f"Remo a una mano {r}", f"Elevaciones Laterales {r}"], "Accesorios": ["Aperturas mancuernas 3x12", "Remo al mentón 3x12", "Press Francés 3x12", "Core colgado 3x15", "Pájaros 3x15"]},
        "Fullbody": {"Base": [f"Peso Muerto {r}", f"Press Banca {r}", f"Sentadilla {r}"], "Accesorios": ["Dominadas 3x8", "Press Militar 3x10", "Curl femoral 3x12", "Gemelos 3x15", "Core 3x15"]}
    }

def generar_rutina_ia(obj, dias):
    rango = {"Hipertrofia": "4x10-12", "Fuerza": "5x3-5", "Músculo Magro": "3x12-15", "Definición": "4x15-20"}
    r = rango.get(obj, "3x12")
    rutinas = obtener_estructura_rutina(r)
    estructura = {3: ["Empuje", "Tracción", "Pierna"], 4: ["Torso", "Pierna", "Empuje", "Tracción"], 5: ["Empuje", "Tracción", "Pierna", "Torso", "Fullbody"]}
    plan = {}
    for i, tipo in enumerate(estructura.get(dias, estructura[3])):
        plan[f"Día {i+1}: {tipo}"] = rutinas[tipo]
    return plan

def generar_dieta_semanal(peso, objetivo):
    dieta = {
        "Desayuno": ["Avena (80g)", "Huevos (3 unidades)", "Fruta"],
        "Almuerzo": ["Yogur griego", "Nueces (30g)"],
        "Comida": ["Arroz (100g en crudo)", "Pechuga de Pollo (200g)", "Verdura"],
        "Merienda": ["Batido de Proteína", "Plátano"],
        "Cena": ["Pescado blanco (200g)", "Patata cocida (200g)", "Ensalada verde"]
    }
    lista = {"Pechuga Pollo": "1.4kg", "Arroz": "700g", "Avena": "560g", "Huevos": "21 un", "Pescado": "1.4kg", "Patatas": "1.4kg"}
    return dieta, lista

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
                    st.session_state.user = user[1]; st.session_state.data = user; st.rerun()
else:
    if 'page' not in st.session_state: st.session_state.page = "Entrenar"
    
    st.markdown('<div class="fixed-menu">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    if c1.button("💪"): st.session_state.page = "Entrenar"
    if c2.button("💊"): st.session_state.page = "Supl"
    if c3.button("📈"): st.session_state.page = "Progreso"
    if c4.button("🥑"): st.session_state.page = "Nutricion"
    if c5.button("⚙️"): st.session_state.page = "Sistema"
    if c6.button("💬"): st.session_state.page = "Chat"
    st.markdown('</div>', unsafe_allow_html=True)

    if
