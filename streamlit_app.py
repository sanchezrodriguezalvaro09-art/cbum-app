import streamlit as st
from supabase import create_client
import pandas as pd 
st.markdown("""
    <style>
    /* Forzar fondo oscuro en el desplegable */
    div[data-baseweb="select"] > div {
        background-color: #1E1E1E !important;
    }
    /* Forzar color de texto negro en la opción seleccionada */
    div[data-baseweb="select"] > div > div > div {
        color: #000000 !important;
    }
    /* Forzar color de texto negro en las opciones del menú desplegado */
    div[role="option"] {
        color: #000000 !important;
    }
    /* Asegurar que las etiquetas sean blancas */
    label {
        color: #FFFFFF !important;
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
