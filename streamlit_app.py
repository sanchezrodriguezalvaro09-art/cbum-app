import streamlit as st
import sqlite3

# Configuración visual
st.set_page_config(page_title="CBum Elite", layout="centered")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #000000 30%, #000033 100%); color: #FFD700; }
    h1, h2, h3 { color: #FFD700 !important; }
    .fixed-menu { 
        position: fixed; bottom: 0; left: 0; width: 100%; 
        background-color: #000000; padding: 15px;
        display: flex; justify-content: space-around;
        border-top: 2px solid #0000FF; z-index: 999;
    }
    .stButton button { color: #FFD700; background-color: #111; border: 1px solid #0000FF; }
    </style>
""", unsafe_allow_html=True)

# Base de datos (v10 para asegurar estructura completa)
conn = sqlite3.connect('fitness_elite_v10.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
             (nombre TEXT PRIMARY KEY, password TEXT, altura REAL, peso REAL, objetivo TEXT, dias INTEGER)''')
conn.commit()

if 'user' not in st.session_state: st.session_state.user = None
if 'page' not in st.session_state: st.session_state.page = "Inicio"

# --- Lógica de IA ampliada ---
def generar_rutina_completa(obj, dias):
    # Más opciones para que la IA sea variada
    rutinas = {
        "Hipertrofia": ["Torso", "Pierna", "Empuje", "Tracción", "Pierna"],
        "Fuerza": ["Básicos A", "Básicos B", "Accesorio A", "Accesorio B", "Básicos C"],
        "Músculo Magro": ["Circuito A", "Circuito B", "Cardio/Core", "Torso", "Pierna"],
        "Definición": ["HIIT 1", "HIIT 2", "Fullbody", "Cardio", "Fullbody"]
    }
    plan = {}
    for i in range(dias):
        musculos = rutinas.get(obj, ["Día genérico"])[i % len(rutinas.get(obj, ["Día genérico"]))]
        plan[f"Día {i+1}: {musculos}"] = ["Press principal 4x10", "Ejercicio accesorio 3x12", "Finalizador 3x15"]
    return plan

# --- Login / Registro ---
if st.session_state.user is None:
    st.title("CBUM ELITE")
    choice = st.radio("Acceso:", ["Iniciar Sesión", "Registrarse"])
    n, p = st.text_input("Usuario"), st.text_input("Contraseña", type="password")
    
    if choice == "Registrarse":
        alt = st.number_input("Altura (cm)", 140, 220, 175)
        peso = st.number_input("Peso actual (kg)", 40.0, 150.0, 70.0)
        obj = st.selectbox("Objetivo", ["Hipertrofia", "Fuerza", "Músculo Magro", "Definición"])
        dias = st.slider("Días de entrenamiento", 3, 5, 4)
        if st.button("Crear cuenta"):
            c.execute("INSERT INTO usuarios VALUES (?,?,?,?,?,?)", (n, p, alt, peso, obj, dias))
            conn.commit()
            st.success("Cuenta creada correctamente.")
    elif st.button("Entrar"):
        c.execute("SELECT objetivo, dias, altura, peso FROM usuarios WHERE nombre=? AND password=?", (n, p))
        res = c.fetchone()
        if res:
            st.session_state.user = n
            st.session_state.obj, st.session_state.dias, st.session_state.alt, st.session_state.peso = res
            st.rerun()
else:
    # Menú inferior fijo
    st.markdown('<div class="fixed-menu">', unsafe_allow_html=True)
    cols = st.columns(4)
    if cols[0].button("💪"): st.session_state.page = "Entrenar"
    if cols[1].button("💊"): st.session_state.page = "Supl"
    if cols[2].button("📈"): st.session_state.page = "Progreso"
    if cols[3].button("💬"): st.session_state.page = "Chat"
    st.markdown('</div>', unsafe_allow_html=True)

    # Contenido según página
    if st.session_state.page == "Inicio":
        st.title(f"Bienvenido, {st.session_state.user}")
        st.write(f"Altura: {st.session_state.alt}cm | Peso: {st.session_state.peso}kg")
        st.write(f"Objetivo: {st.session_state.obj}")
    
    elif st.session_state.page == "Entrenar":
        st.subheader("Rutina Semanal")
        plan = generar_rutina_completa(st.session_state.obj, st.session_state.dias)
        for dia, ejer in plan.items():
            with st.expander(dia):
                for e in ejer: st.write(f"- {e}")

    elif st.session_state.page == "Progreso":
        st.subheader("Seguimiento de Peso")
        st.write("Tu peso inicial fue: " + str(st.session_state.peso) + " kg")
        nuevo_peso = st.number_input("Registrar nuevo peso actual (kg)")
        if st.button("Actualizar seguimiento"):
            st.success(f"Progreso guardado: {nuevo_peso} kg. ¡Vas por buen camino!")

