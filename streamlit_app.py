import streamlit as st
from supabase import create_client
import pandas as pd 
st.markdown("""
    <style>
    /* 1. Fondo del desplegable (caja cerrada) */
    div[data-baseweb="select"] > div {
        background-color: #1E1E1E !important;
    }
    
    /* 2. Color del texto dentro de la caja cerrada (lo que está seleccionado) */
    div[data-baseweb="select"] div[data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
    }
    
    /* 3. Color del texto en la lista desplegada (opciones) */
    div[role="option"] {
        color: #000000 !important;
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
