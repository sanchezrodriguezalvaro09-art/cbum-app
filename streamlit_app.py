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
        "Empuje": {"Base": [f"Press Banca {r}", f"Press Militar {r}", f"Fondos en paralelas {r}"], "Accesorios": ["Press inclinado mancuernas", "Elevaciones laterales", "Extensión tríceps cuerda", "Cruces polea", "Facepull"]},
        "Tracción": {"Base": [f"Dominadas {r}", f"Remo con barra {r}", f"Curl con barra {r}"], "Accesorios": ["Jalón al pecho agarre neutro", "Remo polea baja", "Pájaros (hombro post)", "Curl martillo", "Antebrazo"]},
        "Pierna": {"Base": [f"Sentadilla {r}", f"Prensa {r}", f"Peso Muerto Rumano {r}"], "Accesorios": ["Extensiones cuádriceps", "Curl femoral tumbado", "Gemelos de pie", "Hip thrust", "Abdominales con peso"]},
        "Torso": {"Base": [f"Press Inclinado {r}", f"Remo a una mano {r}", f"Elevaciones Laterales {r}"], "Accesorios": ["Aperturas mancuernas", "Remo al mentón", "Press Francés", "Core colgado", "Pájaros"]},
        "Fullbody": {"Base": [f"Peso Muerto {r}", f"Press Banca {r}", f"Sentadilla {r}"], "Accesorios": ["Dominadas", "Press Militar", "Curl femoral", "Gemelos", "Core"]}
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

    if st.session_state.page == "Entrenar":
        st.subheader(f"Rutina Elite: {st.session_state.data[5]}")
        plan = generar_rutina_ia(st.session_state.data[5], st.session_state.data[6])
        for dia, contenido in plan.items():
            with st.expander(dia):
                st.write("**--- BASE PESADA ---**")
                for e in contenido["Base"]: st.write(f"✅ {e}")
                st.write("**--- ACCESORIOS ---**")
                for ex in contenido["Accesorios"]: st.checkbox(f"{ex}")
    
    elif st.session_state.page == "Supl":
        st.subheader("💊 Plan de Suplementación Personalizado")
        peso_usuario = st.session_state.data[3]
        dias_usuario = st.session_state.data[6]
        # Fórmulas de cálculo ajustadas
        creatina = round(peso_usuario * 0.05, 1)
        proteina = round(peso_usuario * 0.4, 0)
        
        suplementos = {
            "Creatina Monohidrato": {
                "Dosis": f"{creatina}g diarios", 
                "Beneficio": "Mejora la fuerza explosiva y la hidratación muscular, dosificado según tu peso corporal."
            },
            "Proteína Whey": {
                "Dosis": f"{int(proteina)}g post-entreno", 
                "Beneficio": "Aporte rápido de aminoácidos para la síntesis proteica post-entrenamiento."
            },
            "Omega-3": {
                "Dosis": "2g diarios (1g comida, 1g cena)", 
                "Beneficio": "Regulador de la inflamación sistémica, clave para la salud articular."
            }
        }
        for nombre, info in suplementos.items():
            with st.expander(f"✨ {nombre}"):
                st.write(f"**Dosis:** {info['Dosis']}")
                st.write(f"**¿Qué aporta?:** {info['Beneficio']}")
    
    elif st.session_state.page == "Nutricion":
        st.subheader("🥑 Dieta IA y Compra")
        if st.button("Generar Plan Semanal"):
            dieta, lista = generar_dieta_semanal(st.session_state.data[3], st.session_state.data[5])
            for k, v in dieta.items(): st.write(f"**{k}**: {v}")
            st.divider()
            for k, v in lista.items(): st.write(f"🛒 {k}: {v}")

    elif st.session_state.page == "Progreso":
        st.subheader("📊 Historial y Registro")
        try:
            df = pd.read_sql_query("SELECT ejercicio, peso_kg FROM historial_ejercicios_v2 WHERE usuario=?", conn, params=(st.session_state.user,))
            if not df.empty: st.bar_chart(df.set_index('ejercicio'))
        except: st.info("Registra tu primer ejercicio.")
        with st.form("carga"):
            ejer = st.text_input("Ejercicio")
            kilos = st.number_input("Kilos", min_value=0.0)
            reps = st.number_input("Reps", min_value=0)
            rpe = st.slider("RPE", 1, 10, 8)
            if st.form_submit_button("Registrar"):
                c.execute("INSERT INTO historial_ejercicios_v2 (usuario, ejercicio, peso_kg, reps, rpe) VALUES (?, ?, ?, ?, ?)", (st.session_state.user, ejer, kilos, reps, rpe))
                conn.commit()
                st.success("Guardado correctamente")
                st.rerun()

    elif st.session_state.page == "Sistema":
        st.subheader("⚙️ Configuración")
        if st.button("Aplicar Mejora IA"): st.balloons()
    
    elif st.session_state.page == "Chat":
        st.subheader("💬 Coach")
        st.text_input("Pregunta al Coach:")
