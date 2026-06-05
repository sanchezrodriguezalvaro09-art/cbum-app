import streamlit as st

# --- Configuración inicial ---
st.set_page_config(page_title="CBum Elite Training", layout="centered", initial_sidebar_state="collapsed")

# CSS para asegurar visibilidad (letras rojas en caja, negro en opciones)
st.markdown("""
    <style>
    div[data-baseweb="select"] div { color: #FF0000 !important; font-weight: 900 !important; }
    div[role="option"] { color: #000000 !important; font-weight: 900 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>CBUM ELITE TRAINING</h1>", unsafe_allow_html=True)

# --- Módulo de Suplementación ---
st.markdown("### 💊 Protocolo de Suplementación")
peso = st.number_input("Introduce tu peso (kg)", min_value=40, max_value=150, value=93)
objetivo = st.selectbox("Elige tu objetivo:", ["Hipertrofia", "Definición", "Músculo magro"])

if st.button("Calcular dosis seguras"):
    proteina = peso * 1.8
    st.success(f"Proteína recomendada: {proteina:.0f}g diarios")
    st.info("Creatina: 5g diarios (Monohidrato, estándar de seguridad)")

# --- Módulo de Entrenamiento ---
st.markdown("---")

if objetivo:
    st.subheader(f"Rutina enfocada en: {objetivo}")
    
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

    # Mostrar la rutina seleccionada
    for grupo, ejercicios in rutina.items():
        with st.expander(f"Día de {grupo}"):
            for ej in ejercicios:
                st.write(f"✅ {ej}")

    if st.button("Guardar entrenamiento"):
        st.success("¡Entrenamiento guardado con éxito!")


