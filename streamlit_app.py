import streamlit as st
from supabase import create_client
import pandas as pd 
# CSS personalizado para un look "Elite" - Versión forzada
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #0E1117 !important;
        color: #FFFFFF !important;
    }
    
    /* Botones */
    div.stButton > button {
        background-color: #FFD700 !important;
        color: black !important;
        border-radius: 10px !important;
        font-weight: bold !important;
    }

    /* Etiquetas */
    label {
        color: #FFFFFF !important;
    }

    /* Solución definitiva para el desplegable (Selectbox) */
    div[data-baseweb="select"] > div {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #444444 !important;
    }
    
    /* El texto dentro del desplegable cuando se abre */
    div[role="listbox"] {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
    }
    
    /* Elementos dentro de la lista */
    div[role="option"] {
        color: #FFFFFF !important;
        background-color: #1E1E1E !important;
    }

    /* Títulos y texto */
    h1, h2, h3, p, div {
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# Configuración inicial
st.set_page_config(page_title="CBum Elite Training", layout="centered")
st.markdown("<h1 style='text-align: center; color: #FFD700;'>CBUM ELITE TRAINING</h1>", unsafe_allow_html=True)

# Aquí irán tus llaves de Supabase (las que guardaste antes)
# URL y KEY las pondremos de forma segura más adelante
st.write("Bienvenido a tu app de entrenamiento. Configurando base de datos...")

# Módulo de Suplementación Segura
st.markdown("### 💊 Protocolo de Suplementación")
peso = st.number_input("Introduce tu peso (kg)", min_value=40, max_value=150, value=70)
objetivo = st.selectbox("Objetivo", ["Músculo", "Definición"])

if st.button("Calcular dosis seguras"):
    proteina = peso * 1.8
    st.success(f"Proteína recomendada: {proteina:.0f}g diarios")
    st.info("Creatina: 5g diarios (Monohidrato, estándar de seguridad)")
    st.write("Recuerda: Consulta siempre a un profesional de la salud.")

# Módulo de Entrenamiento
st.header("🏋️ Entrenamiento")
ejercicio = st.selectbox("Elige ejercicio", ["Curl Muñeca", "Elevación Talones", "Press Banca", "Sentadilla"])
series = st.slider("Series", 1, 10)
reps = st.slider("Repeticiones", 1, 30)

if st.button("Guardar entrenamiento"):
    st.write(f"Guardado: {ejercicio} | {series} series x {reps} reps")
