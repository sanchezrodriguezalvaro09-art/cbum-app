import streamlit as st

# --- Configuración inicial ---
st.set_page_config(page_title="CBum Elite Training", layout="centered", initial_sidebar_state="collapsed")

# CSS para asegurar que las letras rojas se vean bien
st.markdown("""
    <style>
    div[data-baseweb="select"] div { color: #FF0000 !important; font-weight: 900 !important; }
    div[role="option"] { color: #000000 !important; font-weight: 900 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>CBUM ELITE TRAINING</h1>", unsafe_allow_html=True)

# --- Módulo de Entrada de Datos ---
st.markdown("### 👤 Datos Personales y Objetivos")
peso = st.number_input("Introduce tu peso (kg)", min_value=40, max_value=150, value=70)
altura = st.number_input("Introduce tu altura (cm)", min_value=140, max_value=220, value=175)
objetivo = st.selectbox("Elige tu objetivo:", ["Hipertrofia", "Definición", "Músculo magro"])
equipo = st.selectbox("¿Con qué entrenas?", ["Mancuernas", "Peso libre", "Máquinas"])

# --- Lógica de Generación ---
if st.button("Generar Rutina Completa"):
    # Cálculos rápidos
    proteina = peso * 1.8
    st.success(f"Proteína recomendada: {proteina:.0f}g diarios")
    st.info(f"Ajustando carga para altura: {altura}cm")

    st.markdown("---")
    st.subheader(f"Tu Rutina: {objetivo} con {equipo}")
    
    # Definición de ejercicios basados en el equipo
    if equipo == "Mancuernas":
        pref = "Mancuerna"
    elif equipo == "Peso libre":
        pref = "Barra"
    else:
        pref = "Máquina"
    
    # Estructura de ejercicios
    rutina_base = {
        "Pecho": [f"Press {pref} Inclinado", f"Press {pref} Plano", "Fondos"],
        "Espalda": ["Dominadas", f"Remo con {pref}", "Jalón al pecho"],
        "Hombro": [f"Press {pref} Militar", "Elevaciones laterales"],
        "Pierna": [f"Sentadilla con {pref}", "Prensa", "Curl femoral"],
        "Abdomen": ["Plancha abdominal", "Crunch con peso"],
        "Antebrazo": ["Curl de muñeca", "Paseo del granjero"]
    }

    # Definición de repeticiones según objetivo
    if objetivo == "Hipertrofia":
        esquema = "4x10"
        nota = "🔥 Enfoque: Cargas pesadas, máximo crecimiento."
    elif objetivo == "Definición":
        esquema = "3x15"
        nota = "⚡ Enfoque: Altas repeticiones, menos descanso."
    else:
        esquema = "4x12"
        nota = "🎯 Enfoque: Control total y técnica perfecta."

    st.write(nota)

    # Generación de la rutina
    for grupo, ejercicios in rutina_base.items():
        with st.expander(f"Día de {grupo}"):
            for ej in ejercicios:
                st.write(f"✅ {ej} - {esquema}")

    if st.button("Guardar entrenamiento"):
        st.success("¡Entrenamiento guardado con éxito!")


