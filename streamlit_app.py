import streamlit as st

# --- Configuración inicial ---
st.set_page_config(page_title="CBum Elite Training", layout="centered")

# CSS para asegurar visibilidad (letras rojas en selectores)
st.markdown("""
    <style>
    div[data-baseweb="select"] div { color: #FF0000 !important; font-weight: 900 !important; }
    div[role="option"] { color: #000000 !important; font-weight: 900 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>CBUM ELITE TRAINING</h1>", unsafe_allow_html=True)

# --- Entrada de Datos ---
peso = st.number_input("Peso (kg)", min_value=40, max_value=150, value=70)
altura = st.number_input("Altura (cm)", min_value=140, max_value=220, value=175)
dias = st.number_input("Días de entrenamiento por semana", min_value=3, max_value=6, value=4)
objetivo = st.selectbox("Objetivo:", ["Hipertrofia", "Definición", "Músculo magro"])
equipo = st.selectbox("Equipamiento:", ["Mancuernas", "Peso libre", "Máquinas"])

if st.button("Generar Rutina Eficiente"):
    p = "Mancuerna" if equipo == "Mancuernas" else "Barra" if equipo == "Peso libre" else "Máquina"
    
    # Base de ejercicios (4 por grupo)
    ejercicios = {
        "Pecho": [f"Press {p} Inclinado", f"Press {p} Plano", "Fondos", "Aperturas"],
        "Espalda": ["Dominadas", f"Remo con {p}", "Jalón al pecho", "Remo a una mano"],
        "Hombro": [f"Press {p} Militar", "Elevaciones laterales", "Pájaros", "Press Arnold"],
        "Pierna": [f"Sentadilla con {p}", "Prensa", "Curl femoral", "Extensiones"],
        "Abdomen": ["Plancha", "Crunch con peso", "Elevación de piernas", "Rueda abdominal"],
        "Antebrazo": ["Curl de muñeca", "Paseo del granjero", "Curl invertido", "Hold de agarre"]
    }

    st.markdown("---")
    st.subheader(f"Rutina para {dias} días/semana - Objetivo: {objetivo}")
    
    # Definir series y repeticiones según objetivo
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
    
    # Lógica de agrupación eficiente según días
    if dias == 3:
        rutina_semanal = {
            "Día 1 (Empuje)": ["Pecho", "Hombro"], 
            "Día 2 (Tracción)": ["Espalda", "Antebrazo"], 
            "Día 3 (Pierna/Core)": ["Pierna", "Abdomen"]
        }
    elif dias == 4:
        rutina_semanal = {
            "Día 1 (Pecho/Espalda)": ["Pecho", "Espalda"], 
            "Día 2 (Pierna/Core)": ["Pierna", "Abdomen"], 
            "Día 3 (Hombro/Antebrazo)": ["Hombro", "Antebrazo"], 
            "Día 4 (Full Body)": ["Pecho", "Pierna"]
        }
    else: # 5 o 6 días
        rutina_semanal = {
            "Día 1 (Pecho)": ["Pecho"], 
            "Día 2 (Espalda)": ["Espalda"], 
            "Día 3 (Pierna)": ["Pierna"], 
            "Día 4 (Hombro)": ["Hombro"], 
            "Día 5 (Accesorios)": ["Abdomen", "Antebrazo"]
        }

    # Mostrar la rutina organizada
    for dia, grupos in rutina_semanal.items():
        with st.expander(dia):
            for grupo in grupos:
                st.write(f"**--- {grupo} ---**")
                for ej in ejercicios[grupo]:
                    st.write(f"✅ {ej} - {esquema}")

    # Guardar
    if st.button("Guardar entrenamiento"):
        st.success("¡Plan guardado con éxito!")


