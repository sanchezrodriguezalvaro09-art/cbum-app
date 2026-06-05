import streamlit as st
from supabase import create_client
import pandas as pd 
st.markdown("""
    <style>
    /* Caja cerrada: Texto ROJO para probar visibilidad */
    div[data-baseweb="select"] div {
        color: #FF0000 !important;
        font-weight: 900 !important;
        font-size: 18px !important;
    }
    /* Lista abierta: Texto NEGRO sobre fondo BLANCO */
    div[role="option"] {
        color: #000000 !important;
        background-color: #FFFFFF !important;
        font-weight: 900 !important;
        font-size: 18px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Configuración inicial
st.set_page_config(page_title="CBum Elite Training", layout="centered", initial_sidebar_state="collapsed")
st.markdown("<h1 style='text-align: center; color: #FFD700;'>CBUM ELITE TRAINING</h1>", unsafe_allow_html=True)

# Aquí irán tus llaves de Supabase (las que guardaste antes)
# URL y KEY las pondremos de forma segura más adelante
st.write("Bienvenido a tu app de entrenamiento. Configurando base de datos...")

# Módulo de Suplementación Segura
st.markdown("### 💊 Protocolo de Suplementación")
peso = st.number_input("Introduce tu peso (kg)", min_value=40, max_value=150, value=70)
objetivo = st.selectbox("Elige tu objetivo:", ["Hipertrofia", "Definición", "Músculo magro"])

if st.button("Calcular dosis seguras"):
    proteina = peso * 1.8
    st.success(f"Proteína recomendada: {proteina:.0f}g diarios")
    st.info("Creatina: 5g diarios (Monohidrato, estándar de seguridad)")
    st.write("Recuerda: Consulta siempre a un profesional de la salud.")
# --- Módulo de Entrenamiento Personalizado ---
# --- Módulo de Entrenamiento Personalizado ---
st.markdown("---")
st.subheader(f"Rutina enfocada en: {objetivo}")

# Definimos las rutinas según el objetivo
if objetivo == "Hipertrofia":
    rutina = {
        "Pecho": ["Press Inclinado (4x10)", "Press Plano (4x8)", "Fondos (3x12)"],
        "Espalda": ["Dominadas (4xMax)", "Remo con barra (4x8)", "Jalón al pecho (3x12)"],
        "Hombro": ["Press Militar (4x8)", "Elevaciones laterales (4x15)"],
        "Pierna": ["Sentadilla (4x8)", "Prensa (4x12)"]
    }
    st.write("🔥 **Enfoque Hipertrofia:** Cargas pesadas, máximo crecimiento.")

elif objetivo == "Definición":
    rutina = {
        "Pecho": ["Press Inclinado (3x15)", "Press Plano (3x15)", "Cruce de poleas (3x20)"],
        "Espalda": ["Jalón al pecho (3x15)", "Remo en polea (3x15)", "Facepull (3x20)"],
        "Hombro": ["Press mancuernas (3x15)", "Elevaciones laterales (3x20)"],
        "Pierna": ["Sentadilla (3x15)", "Zancadas (3x15)", "Curl femoral (3x20)"]
    }
    st.write("⚡ **Enfoque Definición:** Altas repeticiones, menos descanso.")

elif objetivo == "Músculo magro":
    rutina = {
        "Pecho": ["Press Inclinado (4x12)", "Press Plano (4x12)", "Fondos (3x12)"],
        "Espalda": ["Dominadas (3x10)", "Remo mancuerna (3x12)", "Jalón al pecho (3x12)"],
        "Hombro": ["Press Militar (3x12)", "Elevaciones laterales (4x12)"],
        "Pierna": ["Sentadilla (4x10)", "Prensa (4x12)", "Curl femoral (3x12)"]
    }
    st.write("🎯 **Enfoque Músculo Magro:** Control total y técnica perfecta.")

# Mostramos la rutina elegida
for grupo, ejercicios in rutina.items():
    with st.expander(f"Día de {grupo}"):
        for ej in ejercicios:
            st.write(f"✅ {ej}")
reps = st.slider("Repeticiones", 1, 30)

if st.button("Guardar entrenamiento"):
    st.write(f"Guardado: {ejercicio} | {series} series x {reps} reps")
