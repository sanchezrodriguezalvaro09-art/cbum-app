import streamlit as st
import sqlite3

# --- 1. CONFIGURACIÓN ELITE (ESTILO VISUAL) ---
st.set_page_config(page_title="CBum Elite Pro", layout="centered")
st.markdown("""
    <style>
    .stApp { background: #000000; color: #FFD700; font-family: 'Arial'; }
    .fixed-menu { position: fixed; bottom: 0; left: 0; width: 100%; background: #0a0a0a; 
                  padding: 15px; display: flex; justify-content: space-around; 
                  border-top: 2px solid #0000FF; z-index: 999; }
    .card { background: #111; padding: 20px; border-left: 5px solid #0000FF; margin-bottom: 10px; }
    h1, h2 { color: #FFD700 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. GESTIÓN DE DATOS (NÚCLEO) ---
conn = sqlite3.connect('cbum_elite_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
             (id INTEGER PRIMARY KEY, nombre TEXT, pass TEXT, peso REAL, altura REAL, objetivo TEXT, dias INTEGER)''')
conn.commit()

# --- 3. MOTOR DE IA (GENERADOR DE RUTINAS) ---
def motor_ia_rutinas(obj, dias):
    # La IA construye el plan basado en tu objetivo
    plan = {
        "Hipertrofia": ["Día 1: Pecho/Tríceps", "Día 2: Espalda/Bíceps", "Día 3: Pierna/Hombro", "Día 4: Fullbody"],
        "Fuerza": ["Día 1: Empuje (Pesado)", "Día 2: Tracción (Pesado)", "Día 3: Pierna (Potencia)", "Día 4: Accesorio"]
    }
    ejercicios = {
        "Pecho/Tríceps": [("Press Banca", "Pecho"), ("Press Inclinado", "Pecho"), ("Extensiones Tríceps", "Tríceps")],
        "Espalda/Bíceps": [("Dominadas", "Espalda"), ("Remo Barra", "Espalda"), ("Curl Barra", "Bíceps")],
        "Pierna/Hombro": [("Sentadilla", "Pierna"), ("Prensa", "Pierna"), ("Press Militar", "Hombro")]
    }
    return plan.get(obj, ["Día genérico"]), ejercicios

# --- 4. INTERFAZ DE USUARIO ---
if 'user' not in st.session_state: st.session_state.user = None

if not st.session_state.user:
    st.title("🚀 CBUM ELITE PRO")
    tab1, tab2 = st.tabs(["ENTRAR", "REGISTRO ELITE"])
    with tab2:
        n = st.text_input("Nombre")
        p = st.text_input("Contraseña", type="password")
        alt = st.number_input("Altura (cm)", 150, 220, 180)
        pes = st.number_input("Peso (kg)", 50.0, 150.0, 80.0)
        obj = st.selectbox("Objetivo", ["Hipertrofia", "Fuerza"])
        dias = st.slider("Días de entreno", 3, 5, 4)
        if st.button("Registrar"):
            c.execute("INSERT INTO usuarios (nombre, pass, peso, altura, objetivo, dias) VALUES (?,?,?,?,?,?)", (n, p, pes, alt, obj, dias))
            conn.commit()
            st.success("Cuenta creada.")
    with tab1:
        un = st.text_input("User")
        up = st.text_input("Pass", type="password")
        if st.button("Acceder"):
            c.execute("SELECT * FROM usuarios WHERE nombre=? AND pass=?", (un, up))
            user = c.fetchone()
            if user:
                st.session_state.user = user[1]
                st.session_state.data = user
                st.rerun()

else:
    # --- 5. NAVEGACIÓN Y VISTAS ELITE ---
    if 'page' not in st.session_state: st.session_state.page = "Entrenar"

    # Menú Fijo Inferior
    st.markdown('<div class="fixed-menu">', unsafe_allow_html=True)
    cols = st.columns(4)
    if cols[0].button("💪"): st.session_state.page = "Entrenar"
    if cols[1].button("💊"): st.session_state.page = "Supl"
    if cols[2].button("📈"): st.session_state.page = "Progreso"
    if cols[3].button("💬"): st.session_state.page = "Chat"
    st.markdown('</div>', unsafe_allow_html=True)

    # Lógica de pantallas
    if st.session_state.page == "Entrenar":
        st.subheader("Rutina de Élite")
        dias_plan, ejercicios = motor_ia_rutinas(st.session_state.data[5], st.session_state.data[6])
        for dia in dias_plan[:st.session_state.data[6]]:
            with st.expander(dia):
                st.write("Ejercicios recomendados:")
                for ej, musc in ejercicios.get(dia.split(": ")[1], [("Ej. Global", "General")]):
                    st.markdown(f"<div class='card'><b>{ej}</b><br><small>Enfoque: {musc}</small></div>", unsafe_allow_html=True)

    elif st.session_state.page == "Progreso":
        st.subheader("Tu Seguimiento")
        st.metric("Peso Inicial", f"{st.session_state.data[3]} kg")
        st.write("IA: Analizando tu evolución semanal...")

