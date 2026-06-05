import streamlit as st
import time

# --- Configuración inicial ---
st.set_page_config(page_title="CBum Elite Training", layout="centered")

st.markdown("""
    <style>
    div[data-baseweb="select"] div { color: #FF0000 !important; font-weight: 900 !important; }
    h1 { color: #FFD700; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>CBUM ELITE TRAINING</h1>", unsafe_allow_html=True)

# --- Entrada de Datos ---
col1, col2 = st.columns(2)
with col1:
    peso_corp = st.number_input("Peso corporal (kg)", 40, 150, 70)
    altura = st.number_input("Altura (cm)", 140, 220, 175)
with col2:
    dias = st.number_input("Días por semana", 3, 6, 4)
    nivel = st.select_slider("Nivel", options=["Principiante", "Intermedio", "Avanzado"])

objetivo = st.selectbox("Objetivo:", ["Hipertrofia", "Definición", "Músculo magro"])
equipo = st.selectbox("Equipamiento:", ["Mancuernas", "Peso libre", "Máquinas"])

if st.button("Generar Plan de Élite"):
    # --- Suplementación ---
    st.markdown("---")
    st.markdown("### 💊 Protocolo de Suplementación")
    proteina = peso_corp * 1.8
    st.success(f"Proteína recomendada: {proteina:.0f}g diarios")
    st.info("Creatina: 5g diarios (Monohidrato, estándar de seguridad)")
    st.write("⚠️ *Recuerda: Toma tu suplementación post-entrenamiento para mejor absorción.*")

    # --- Lógica de Entrenamiento ---
    series_reps = "3x12" if nivel == "Principiante" else "4x10" if nivel == "Intermedio" else "5x10 con Drop-sets"
    
    st.markdown("---")
    st.subheader(f"Rutina para {dias} días - {objetivo}")

    # Temporizador
    if st.button("⏱️ Iniciar descanso (90s)"):
        with st.empty():
            for s in range(90, 0, -1):
                st.write(f"⏳ Descanso: {s}s")
                time.sleep(1)
            st.write("¡A por la siguiente serie!")

    ejercicios = {
        "Pecho": ["Press Inclinado", "Press Plano", "Fondos", "Aperturas"],
        "Espalda": ["Dominadas", "Remo", "Jalón al pecho", "Remo a una mano"],
        "Bíceps": ["Curl Barra", "Curl Martillo", "Curl Scott", "Curl Inclinado"],
        "Tríceps": ["Press Francés", "Ext. Polea", "Dips", "Ext. Tras nuca"],
        "Pierna": ["Sentadilla", "Prensa", "Curl femoral", "Extensiones"],
        "Abdomen": ["Plancha", "Crunch", "Elev. piernas", "Rueda"],
        "Antebrazo": ["Curl muñeca", "Paseo granjero", "Curl invertido", "Hold agarre"]
    }

    # Asignación exacta según días
    if dias == 3:
        rutina_map = {"Día 1": ["Pecho", "Tríceps"], "Día 2": ["Espalda", "Bíceps"], "Día 3": ["Pierna", "Abdomen", "Antebrazo"]}
    elif dias == 4:
        rutina_map = {"Día 1": ["Pecho", "Tríceps"], "Día 2": ["Espalda", "Bíceps"], "Día 3": ["Pierna"], "Día 4": ["Abdomen", "Antebrazo"]}
    elif dias == 5:
        rutina_map = {"Día 1": ["Pecho", "Tríceps"], "Día 2": ["Espalda", "Bíceps"], "Día 3": ["Pierna"], "Día 4": ["Hombro"], "Día 5": ["Abdomen", "Antebrazo"]}
    else:
        rutina_map = {"Día 1": ["Pecho"], "Día 2": ["Espalda"], "Día 3": ["Pierna"], "Día 4": ["Hombro"], "Día 5": ["Bíceps", "Tríceps"], "Día 6": ["Abdomen", "Antebrazo"]}

    # Visualización
    for dia, grupos in rutina_map.items():
        with st.expander(f"{dia} - Sesión"):
            for grupo in grupos:
                st.write(f"#### {grupo}")
                for ej in ejercicios.get(grupo, []):
                    col1, col2, col3 = st.columns([0.5, 3, 1.5])
                    with col1:
                        st.checkbox("✅", key=f"check_{dia}_{ej}")
                    with col2:
                        st.write(f"**{ej}** ({series_reps})")
                    with col3:
                        st.number_input("kg", key=f"peso_{dia}_{ej}", min_value=0.0, step=0.5)

    st.success("¡Plan guardado! Registra tus pesos cada día para ver tu evolución.")


