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
    variante = "Estándar"
    if len(historial_fuerza) >= 5:
        pesos = [h[1] for h in historial_fuerza[:5]]
        if all(x <= pesos[0] for x in pesos[1:]): variante = "Avanzada"
    rango = {"Hipertrofia": "4x10-12", "Fuerza": "5x3-5", "Músculo Magro": "3x10-15", "Definición": "4x15-20"}
    r = rango.get(obj, "3x12")
    
    ejercicios_base = {
        "Empuje": [f"Press Banca {r}", f"Press Militar {r}", f"Fondos {r}"],
        "Tracción": [f"Dominadas {r}", f"Remo Barra {r}", f"Curl Bíceps {r}"],
        "Pierna": [f"Sentadilla {r}", f"Prensa {r}", f"Peso Muerto Rumano {r}"],
        "Torso": [f"Press Inclinado {r}", f"Jalón al pecho {r}", f"Elevaciones Laterales {r}"],
        "Fullbody": [f"Peso Muerto {r}", f"Press Banca {r}", f"Remo {r}"]
    }
    opcionales = {
        "Empuje": ["Cruces polea", "Elev. frontales", "Ext. tríceps"],
        "Tracción": ["Facepull", "Pájaros", "Curl martillo"],
        "Pierna": ["Curl femoral", "Ext. cuádriceps", "Gemelos"],
        "Torso": ["Flexiones", "Remo mentón", "Plancha"],
        "Fullbody": ["Burpees", "Saltos cajón", "Abdominales"]
    }
    estructura = {3: ["Empuje", "Tracción", "Pierna"], 4: ["Torso", "Pierna", "Empuje", "Tracción"], 5: ["Empuje", "Tracción", "Pierna", "Torso", "Fullbody"]}
    plan = {}
    dias_sel = estructura.get(dias, estructura[3])
    for i, tipo in enumerate(dias_sel):
        plan[f"Día {i+1}: {tipo}"] = {"base": ejercicios_base[tipo], "extras": opcionales[tipo]}
    return plan

def generar_dieta_semanal(peso, objetivo):
    dieta = {
        "Desayuno": ["Avena (80g)", "Huevos (3 unidades)", "Fruta"],
        "Almuerzo": ["Yogur griego", "Nueces"],
        "Comida": ["Arroz (100g)", "Pollo (200g)", "Verdura"],
        "Merienda": ["Batido Proteína", "Plátano"],
        "Cena": ["Pescado (200g)", "Patata (200g)", "Ensalada"]
    }
    lista = {"Pollo": "1.4kg", "Arroz": "700g", "Avena": "560g", "Huevos": "21 un", "Pescado": "1.4kg", "Patatas": "1.4kg"}
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

    if st.session_state.page == "Entrenar":
        historial = c.execute("SELECT ejercicio, peso_kg, reps FROM historial_ejercicios WHERE usuario=?", (st.session_state.user,)).fetchall()
        st.subheader(f"Rutina Elite: {st.session_state.data[5]}")
        plan = generar_rutina_ia(st.session_state.data[5], st.session_state.data[6], historial)
        for dia, contenido in plan.items():
            with st.expander(dia):
                for e in contenido["base"]: st.write(f"✅ {e}")
                st.write("--- Opcionales ---")
                for ex in contenido["extras"]: st.checkbox(f"Accesorios: {ex}")
    
    elif st.session_state.page == "Supl":
        st.subheader("Plan Suplementación")
        for n, d in {"Creatina": "5g", "Proteína": "30g"}.items(): st.write(f"💊 {n}: {d}")
    
    elif st.session_state.page == "Nutricion":
        st.subheader("🥑 Dieta y Compra")
        if st.button("Generar Plan"):
            dieta, lista = generar_dieta_semanal(st.session_state.data[3], st.session_state.data[5])
            for k, v in dieta.items(): st.write(f"**{k}**: {v}")
            st.subheader("🛒 Lista")
            for k, v in lista.items(): st.write(f"{k}: {v}")

    elif st.session_state.page == "Progreso":
        st.subheader("📊 Progreso")
        with st.form("carga"):
            ejer, kilos = st.text_input("Ejercicio"), st.number_input("Kilos")
            if st.form_submit_button("Registrar"):
                c.execute("INSERT INTO historial_ejercicios (usuario, ejercicio, peso_kg, reps, rpe) VALUES (?,?,?,?,?)", (st.session_state.user, ejer, kilos, 10, 8))
                conn.commit(); st.rerun()

    elif st.session_state.page == "Sistema":
        if st.button("Actualizar"): st.balloons()
    
    elif st.session_state.page == "Chat":
        st.text_input("Pregunta al Coach:")
