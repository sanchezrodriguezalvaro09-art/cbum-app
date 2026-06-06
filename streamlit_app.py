import streamlit as st
import sqlite3
import datetime

st.set_page_config(page_title="CBum Elite Training", layout="wide")

# --- CSS para Menú Fijo Inferior ---
st.markdown("""
    <style>
    .fixed-menu {
        position: fixed; bottom: 0; left: 0; width: 100%;
        background-color: #0e1117; padding: 10px;
        display: flex; justify-content: space-around;
        border-top: 2px solid #333; z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

# --- Base de Datos ---
conn = sqlite3.connect('fitness_elite.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (nombre TEXT PRIMARY KEY, password TEXT, peso_inicial REAL, objetivo TEXT, dias_entreno INTEGER)''')
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
        dias = st.slider("Días de entreno", 3, 6, 4)
        obj = st.selectbox("Objetivo", ["Hipertrofia", "Fuerza", "Músculo Magro", "Definición"])
        if st.button("Registrarse"):
            c.execute("INSERT INTO usuarios VALUES (?,?,?,?,?)", (n, p, peso, obj, dias))
            conn.commit()
            st.success("Registrado.")
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
    st.title(f"Bienvenido, {st.session_state.user}")
    user_info = c.execute("SELECT objetivo, dias_entreno FROM usuarios WHERE nombre=?", (st.session_state.user,)).fetchone()
    
    # --- MENÚ INFERIOR FIJO ---
    st.markdown('<div class="fixed-menu">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("💪 Entrenar"): st.session_state.page = "Entrenar"
    if c2.button("💊 Supl."): st.session_state.page = "Supl"
    if c3.button("📈 Progreso"): st.session_state.page = "Progreso"
    if c4.button("💬 Chat AI"): st.session_state.page = "Chat"
    st.markdown('</div>', unsafe_allow_html=True)

    # --- LÓGICA DE CONTENIDO ---
    if st.session_state.page == "Entrenar":
        st.subheader(f"Rutina: {user_info[0]} ({user_info[1]} días)")
        st.write("La IA ha generado tu rutina de hoy:")
        ejercicios = ["Press Banca", "Sentadilla", "Remo con barra", "Press Militar"] if user_info[0] == "Hipertrofia" else ["Peso Muerto", "Sentadilla", "Press Banca"]
        for ej in ejercicios:
            st.write(f"✅ {ej} - 3 series x 10 repeticiones")
            
    elif st.session_state.page == "Supl":
        st.subheader("Suplementación")
        st.write("• **Proteína:** 30g post-entreno")
        st.write("• **Creatina:** 5g diarios")
        if st.button("Desactivar avisos"): st.success("Avisos desactivados hasta mañana.")

    elif st.session_state.page == "Progreso":
        st.subheader("Tu Evolución")
        peso_c = st.number_input("Peso actual (kg)")
        if st.button("Guardar"):
            c.execute("INSERT INTO progreso_semanal VALUES (?,?,?)", (st.session_state.user, str(datetime.date.today()), peso_c))
            conn.commit()
            st.success("Progreso registrado.")

    elif st.session_state.page == "Chat":
        st.subheader("Asistente IA")
        query = st.text_input("¿Duda de tu rutina?")
        if query: st.write("🤖 IA: Basado en tu objetivo de " + user_info[0] + ", mantén la intensidad.")

