import streamlit as st

# --- Configuración inicial ---
st.set_page_config(page_title="CBum Elite Training", layout="centered")

# CSS para asegurar visibilidad (letras rojas)
st.markdown("""
    <style>
    div[data-baseweb="select"] div { color: #FF0000 !important; font-weight: 900 !important; }
    div[role="option"] { color: #000000 !important; font-weight: 900 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>CBUM ELITE TRAINING</h1>", unsafe_allow_html=True)

# --- Entrada de Datos ---
st.markdown("### 👤 Datos Personales")
peso = st.number_input("Peso (kg)", min_value=40, max_value=150, value=70)
altura = st.number_input("Altura (cm)", min_value=140, max_value=220, value=175)
dias = st.number_input("Días de entrenamiento por semana", min_value=3, max_value=6, value=4)
objetivo = st.selectbox("Objetivo:", ["Hipertrofia", "Definición", "Músculo magro"])
equipo = st.selectbox("Equipamiento:", ["Mancuernas", "Peso libre", "Máquinas"])

if st.button("Generar Plan Completo"):
    # Suplementación
    st.markdown("---")
    st.markdown("### 💊 Protocolo de Suplementación")
    proteina = peso * 1.8
    st.success(f"Proteína recomendada: {proteina:.0f}g diarios")
    st.info("Creatina: 5g diarios (Monohidrato, estándar de seguridad)")

    # Base de ejercicios (4 por grupo, cabezas completas)
    ejercicios = {
        "Pecho": [("Press Inclinado", "https://img.icons8.com/color/96/bench-press.png"), ("Press Plano", "https://img.icons8.com/color/96/bench-press.png"), ("Fondos", "https://img.icons8.com/color/96/pushups.png"), ("Aperturas", "https://img.icons8.com/color/96/dumbbell.png")],
        "Espalda": [("Dominadas", "https://img.icons8.com/color/96/pullups.png"), ("Remo", "https://img.icons8.com/color/96/barbell.png"), ("Jalón al pecho", "https://img.icons8.com/color/96/pullups.png"), ("Remo a una mano", "https://img.icons8.com/color/96/dumbbell.png")],
        "Bíceps": [("Curl Barra (C. Larga)", "https://img.icons8.com/color/96/barbell.png"), ("Curl Martillo (Braquial)", "https://img.icons8.com/color/96/dumbbell.png"), ("Curl Scott (C. Corta)", "https://img.icons8.com/color/96/bicep-curl.png"), ("Curl Inclinado", "https://img.icons8.com/color/96/dumbbell.png")],
        "Tríceps": [("Press Francés (C. Larga)", "https://img.icons8.com/color/96/barbell.png"), ("Ext. Polea (C. Lateral)", "https://img.icons8.com/color/96/pullups.png"), ("Dips (C. Medial)", "https://img.icons8.com/color/96/pushups.png"), ("Ext. Tras nuca", "https://img.icons8.com/color/96/dumbbell.png")],
        "Pierna": [("Sentadilla", "https://img.icons8.com/color/96/squats.png"), ("Prensa", "https://img.icons8.com/color/96/leg-press.png"), ("Curl femoral", "https://img.icons8.com/color/96/leg-curl.png"), ("Extensiones", "https://img.icons8.com/color/96/leg-extensions.png")],
        "Abdomen": [("Plancha", "https://img.icons8.com/color/96/plank.png"), ("Crunch", "https://img.icons8.com/color/96/situps.png"), ("Elevación piernas", "https://img.icons8.com/color/96/situps.png"), ("Rueda abdominal", "https://img.icons8.com/color/96/ab-wheel.png")],
        "Antebrazo": [("Curl muñeca", "https://img.icons8.com/color/96/dumbbell.png"), ("Paseo granjero", "https://img.icons8.com/color/96/dumbbell.png"), ("Curl invertido", "https://img.icons8.com/color/96/barbell.png"), ("Hold agarre", "https://img.icons8.com/color/96/dumbbell.png")]
    }

    esquema = "4x10" if objetivo == "Hipertrofia" else "3x15" if objetivo == "Definición" else "4x12"
    
    st.markdown("---")
    st.subheader(f"Rutina para {dias} días/semana - {objetivo}")
    
    # Lógica de agrupación según los días exactos introducidos
    if dias == 3:
        rutina_semanal = {"Día 1 (Empuje)": ["Pecho", "Tríceps"], "Día 2 (Tracción)": ["Espalda", "Bíceps"], "Día 3 (Pierna/Core)": ["Pierna", "Abdomen", "Antebrazo"]}
    elif dias == 4:
        rutina_semanal = {"Día 1 (Pecho/Tríceps)": ["Pecho", "Tríceps"], "Día 2 (Espalda/Bíceps)": ["Espalda", "Bíceps"], "Día 3 (Pierna)": ["Pierna"], "Día 4 (Core/Accesorios)": ["Abdomen", "Antebrazo"]}
    elif dias == 5:
        rutina_semanal = {"Día 1": ["Pecho", "Tríceps"], "Día 2": ["Espalda", "Bíceps"], "Día 3": ["Pierna"], "Día 4": ["Hombro"], "Día 5": ["Abdomen", "Antebrazo"]}
    else:
        rutina_semanal = {"Día 1": ["Pecho"], "Día 2": ["Espalda"], "Día 3": ["Pierna"], "Día 4": ["Hombro"], "Día 5": ["Bíceps", "Tríceps"], "Día 6": ["Abdomen", "Antebrazo"]}

    for dia, grupos in rutina_semanal.items():
        with st.expander(dia):
            for grupo in grupos:
                st.write(f"### {grupo}")
                for nombre, url in ejercicios.get(grupo, []):
                    col1, col2 = st.columns([1, 4])
                    col1.image(url, width=50)
                    col2.write(f"**{nombre}** ({esquema})")

    if st.button("Guardar mi rutina"):
        st.success("¡Rutina guardada! A darle duro.")


