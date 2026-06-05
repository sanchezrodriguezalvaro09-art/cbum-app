import streamlit as st
import time

st.set_page_config(page_title="CBum Elite Training", layout="centered")

# --- CSS de Élite ---
st.markdown("""
    <style>
    div[data-baseweb="select"] div { color: #FF0000 !important; font-weight: 900 !important; }
    h1 { color: #FFD700; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>CBUM ELITE TRAINING</h1>", unsafe_allow_html=True)

# --- Entrada de Datos ---
peso_corp = st.number_input("Peso corporal (kg)", 40, 150, 70)
altura = st.number_input("Altura (cm)", 140, 220, 175)
nivel = st.select_slider("Nivel de entrenamiento", options=["Principiante", "Intermedio", "Avanzado"])
dias = st.number_input("Días por semana", 3, 6, 4)
objetivo = st.selectbox("Objetivo:", ["Hipertrofia", "Definición", "Músculo magro"])
equipo = st.selectbox("Equipamiento:", ["Mancuernas", "Peso libre", "Máquinas"])

if st.button("Generar Plan de Élite"):
    # Lógica de carga según nivel
    series_reps = "3x12" if nivel == "Principiante" else "4x10" if nivel == "Intermedio" else "5x10 con Drop-sets"
    
    st.markdown("---")
    
    # --- Temporizador ---
    if st.button("⏱️ Iniciar descanso (90s)"):
        with st.empty():
            for seconds in range(90, 0, -1):
                st.write(f"⏳ Descanso: {seconds}s")
                time.sleep(1)
            st.write("¡A por la siguiente serie!")

    # Base de ejercicios
    ejercicios = {
        "Pecho": ["Press Inclinado", "Press Plano", "Fondos", "Aperturas"],
        "Espalda": ["Dominadas", "Remo", "Jalón al pecho", "Remo a una mano"],
        "Bíceps": ["Curl Barra", "Curl Martillo", "Curl Scott", "Curl Inclinado"],
        "Tríceps": ["Press Francés", "Ext. Polea", "Dips", "Ext. Tras nuca"],
        "Pierna": ["Sentadilla", "Prensa", "Curl femoral", "Extensiones"],
        "Abdomen": ["Plancha", "Crunch", "Elev. piernas", "Rueda"],
        "Antebrazo": ["Curl muñeca", "Paseo granjero", "Curl invertido", "Hold agarre"]
    }

    # Estructura días
    rutina_map = {
        3: {"Día 1": ["Pecho", "Tríceps"], "Día 2": ["Espalda", "Bíceps"], "Día 3": ["Pierna", "Abdomen", "Antebrazo"]},
        4: {"Día 1": ["Pecho", "Tríceps"], "Día 2": ["Espalda", "Bíceps"], "Día 3": ["Pierna"], "Día 4": ["Abdomen", "Antebrazo"]}
    }.get(dias, {"Día 1": ["Pecho", "Espalda", "Pierna"]})

    # --- Rutina con Checklist y Peso ---
    for dia, grupos in rutina_map.items():
        with st.expander(f"{dia} - Sesión de entrenamiento"):
            for grupo in grupos:
                st.subheader(grupo)
                for ej in ejercicios[grupo]:
                    col1, col2, col3 = st.columns([0.5, 3, 1.5])
                    with col1:
                        st.checkbox("Done", key=f"check_{dia}_{ej}")
                    with col2:
                        st.write(f"**{ej}** ({series_reps})")
                    with col3:
                        st.number_input("kg", key=f"peso_{dia}_{ej}", min_value=0.0, step=0.5)

    st.success("Nota: Tus pesos se guardan en la sesión. ¡Supera tu marca la próxima semana!")


