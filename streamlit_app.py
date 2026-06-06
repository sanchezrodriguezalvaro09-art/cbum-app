import streamlit as st
import sqlite3
import datetime

st.set_page_config(page_title="CBum Elite Training", layout="wide")

# --- CSS Menú Fijo Inferior ---
st.markdown("""
    <style>
    .fixed-menu { position: fixed; bottom: 0; left: 0; width: 100%; background-color: #0e1117; 
                  padding: 10px; display: flex; justify-content: space-around; 
                  border-top: 2px solid #333; z-index: 999; }
    </style>
""", unsafe_allow_html=True)

# --- Base de Datos ---
conn = sqlite3.connect('fitness_elite_v4.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
             (nombre TEXT PRIMARY KEY, password TEXT, peso_inicial REAL, altura REAL, objetivo TEXT, dias_entreno INTEGER, peso_meta REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS progreso_semanal (usuario TEXT, fecha TEXT, peso_actual REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS registros (usuario TEXT, fecha TEXT, ejercicio TEXT, peso REAL)''')
conn.commit()

if 'user' not in st.session_state: st.session_state.user = None
if 'page' not in st.session_state: st.session_state.page = "Entrenar"

# --- LOGIN / REGISTRO ---
if st.session_state.user is None:
    st.title("CBUM ELITE TRAINING")
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    with tab2:
        n = st.text_input("Usuario", key="rn")
        p = st.text_input("Contraseña", type="password", key="rp")
        peso = st.number_input("Peso inicial (kg)", 40.0, 150.0, 70.0)
        alt = st.number_input("Altura (cm)", 140, 220, 175)
        dias = st.slider("Días de entreno", 3, 6, 4)
        obj = st.selectbox("Objetivo", ["Hipertrofia", "Fuerza", "Músculo Magro", "Definición"])
        meta = st.number_input("Peso meta (kg)", 40.0, 150.0, 75.0)
        if st.button("Registrarse"):
            try:
                c.execute("INSERT INTO usuarios VALUES (?,?,?,?,?,?,?)", (n, p, peso, alt, obj, dias, meta))
                conn.commit()
                st.success("Registrado. Inicia sesión.")
            except: st.error("Usuario existente.")
    with tab1:
        u = st.text_input("Usuario", key="un")
        pw = st.text_input("Contraseña", type="password", key="up")
        if st.button("Entrar"):
            c.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?", (u, pw))
            if c.fetchone():
                st.session_state.user = u
                st.rerun()

# --- APP PRINCIPAL ---
else:
    user_info = c.execute("SELECT objetivo FROM usuarios WHERE nombre=?", (st.session_state.user,)).fetchone()
    
    # Renderizado del Menú Fijo
    st.markdown('<div class="fixed-menu">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("💪"): st.session_state.page = "Entrenar"
    if c2.button("💊"): st.session_state.page = "Supl"
    if c3.button("📈"): st.session_state.page = "Progreso"
    if c4.button("💬"): st.session_state.page = "Chat"
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.page == "Entrenar":
        st.subheader("Rutina de Entrenamiento")
        st.write(f"Objetivo: {user_info[0]}")
        # Lógica IA de rutina
        rutinas = {
            "Hipertrofia": ["Press Banca", "Sentadilla", "Remo", "Press Militar"],
            "Fuerza": ["Peso Muerto", "Sentadilla Pesada", "Press Banca"],
            "Músculo Magro": ["Press Inclinado", "Jalón al pecho", "Zancadas"],
            "Definición": ["Circuito HIIT", "Press con mancuernas", "Cardio"]
        }
        for ej in rutinas.get(user_info[0], ["Ejercicio base"]):
            st.write(f"✅ {ej}: 3 series x 10 repeticiones")
            
    elif st.session_state.page == "Supl":
        st.subheader("Suplementación")
        st.write("• Creatina: 5g al día")
        st.write("• Proteína: 1 scoop post-entreno")
        if st.button("Desactivar avisos"): st.success("Avisos pausados.")

    elif st.session_state.page == "Progreso":
        st.subheader("Tu Evolución")
        peso_c = st.number_input("Peso actual (kg)")
        if st.button("Guardar peso semanal"):
            c.execute("INSERT INTO progreso_semanal VALUES (?,?,?)", (st.session_state.user, str(datetime.date.today()), peso_c))
            conn.commit()
            st.success("Peso guardado.")

    elif st.session_state.page == "Chat":
        st.subheader("Asistente IA")
        query = st.text_input("¿Alguna duda?")
        if query: st.write("🤖 IA: Analizando tus datos de " + user_info[0] + "...")

