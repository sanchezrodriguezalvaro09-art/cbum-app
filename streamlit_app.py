import streamlit as st

# --- Configuración inicial ---
st.set_page_config(page_title="CBum Elite Training", layout="centered")

st.markdown("""
    <style>
    div[data-baseweb="select"] div { color: #FF0000 !important; font-weight: 900 !important; }
    div[role="option"] { color: #000000 !important; font-weight: 900 !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FFD700;'>CBUM ELITE TRAINING</h1>", unsafe_allow_html=True)

# --- Entrada de Datos ---
peso = st.number_input("Peso (kg)", min_value=40, max_value=150, value=70)
dias = st.number_input("Días de entrenamiento/semana", min_value=3, max_value=6, value=4)
objetivo = st.selectbox("Objetivo:", ["Hipertrofia", "Definición", "Músculo magro"])
equipo = st.selectbox("Equipamiento:", ["Mancuernas", "Peso libre", "Máquinas"])

if st.button("Generar Rutina Pro"):
    p = "Mancuerna" if equipo == "Mancuernas" else "Barra" if equipo == "Peso libre" else "Máquina"
    
    # Base de ejercicios completa incluyendo cabezas de Bíceps/Tríceps
    # Usamos URLs de ejemplo para las imágenes
    ejercicios = {
        "Pecho": [("Press Inclinado", "https://i.imgur.com/y4dKq0c.png"), ("Press Plano", "https://i.imgur.com/j4oGq0e.png"), ("Fondos", "https://i.imgur.com/k2pQ9m.png"), ("Aperturas", "https://i.imgur.com/l5rT2p.png")],
        "Espalda": [("Dominadas", "https://i.imgur.com/a1sD3f.png"), ("Remo", "https://i.imgur.com/z9xV8c.png"), ("Jalón al pecho", "https://i.imgur.com/q1wE2r.png"), ("Remo a una mano", "https://i.imgur.com/b7nK4m.png")],
        "Bíceps": [("Curl Barra (Cabeza Larga)", "https://i.imgur.com/c1vB2n.png"), ("Curl Martillo (Braquial)", "https://i.imgur.com/x4zC5m.png"), ("Curl Scott (Cabeza Corta)", "https://i.imgur.com/m9lN8b.png"), ("Curl Inclinado", "https://i.imgur.com/k2jH7g.png")],
        "Tríceps": [("Press Francés (Cabeza Larga)", "https://i.imgur.com/p0oI9u.png"), ("Extensiones polea (Cabeza Lateral)", "https://i.imgur.com/w8eR7t.png"), ("Dips (Cabeza Medial)", "https://i.imgur.com/q6wE5r.png"), ("Extensiones tras nuca", "https://i.imgur.com/t4rE3w.png")],
        "Pierna": [("Sentadilla", "https://i.imgur.com/r5tY4u.png"), ("Prensa", "https://i.imgur.com/f3gH2j.png"), ("Curl femoral", "https://i.imgur.com/d9sA8d.png"), ("Extensiones", "https://i.imgur.com/c7vB6n.png")],
        "Abdomen": [("Plancha", "https://i.imgur.com/n1mK2l.png"), ("Crunch", "https://i.imgur.com/o3pL4k.png"), ("Elevación piernas", "https://i.imgur.com/j5hG6f.png"), ("Rueda", "https://i.imgur.com/d7sA8f.png")]
    }

    esquema = "4x10" if objetivo == "Hipertrofia" else "3x15" if objetivo == "Definición" else "4x12"
    
    st.subheader(f"Rutina enfocada en: {objetivo}")
    
    # Lógica de agrupación simplificada para incluir nuevos grupos
    rutina_semanal = {
        "Día 1 (Torso)": ["Pecho", "Espalda"], 
        "Día 2 (Pierna/Core)": ["Pierna", "Abdomen"], 
        "Día 3 (Brazos)": ["Bíceps", "Tríceps"]
    }

    for dia, grupos in rutina_semanal.items():
        with st.expander(dia):
            for grupo in grupos:
                st.write(f"### {grupo}")
                for nombre, url in ejercicios[grupo]:
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.image(url, width=80)
                    with col2:
                        st.write(f"**{nombre}**\n{esquema}")

    if st.button("Guardar plan"):
        st.success("¡Plan profesional guardado!")


