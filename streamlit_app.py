import streamlit as st
import sqlite3

# Configuración de página
st.set_page_config(page_title="CBum Elite", layout="centered")

# --- Estilos (Fondo negro, letras amarillas y Menú fijo abajo) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #000000 30%, #000033 100%); color: #FFD700; }
    h1, h2, h3 { color: #FFD700 !important; }
    .fixed-menu { 
        position: fixed; bottom: 0; left: 0; width: 100%; 
        background-color: #000000; padding: 10px;
        display: flex; justify-content: space-around;
        border-top: 2px solid #0000FF; z-index: 999;
    }
    .stButton button { color: #FFD700; background-color: #111; border: 1px solid #0000FF; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- Base de Datos ---
conn = sqlite3.connect('fitness_elite_v8.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (nombre TEXT PRIMARY KEY, password TEXT, objetivo TEXT)''')
conn.commit()

if 'user' not in st.session_state: st.session_state.user = None
if 'page' not in st.session_state: st.session_state.page = "Inicio"

# --- LOGIN / REGISTRO ---
if st.session_state.user is None:
    st.title("CBUM ELITE")
    choice = st.radio("Acceso:", ["Iniciar Sesión", "Registrarse"])
    n = st.text_input("Usuario")
    p = st.text_input("Contraseña", type="password")
    
    if choice == "Registrarse":
        obj = st.selectbox("Objetivo", ["Hipertrofia", "Fuerza", "Músculo Magro", "Definición"])
        if st.button("Crear cuenta"):
            try:
                c.execute("INSERT INTO usuarios VALUES (?,?,?)", (n, p, obj))
                conn.commit()
                st.success("Cuenta creada.")
            except: st.error("Error al registrar.")
    else:
        if st.button("Entrar"):
            c.execute("SELECT objetivo FROM usuarios WHERE nombre=? AND password=?", (n, p))
            data = c.fetchone()
            if data:
                st.session_state.user = n
                st.session_state.obj = data[0]
                st.rerun()
            else: st.error("Error en login.")

# --- APP PRINCIPAL ---
else:
    # Contenido principal
    if st.session_state.page == "Inicio":
        st.title(f"Bienvenido, {st.session_state.user}")
        st.write(f"Tu objetivo: {st.session_state.obj}")
    
    elif st.session_state.page == "Entrenar":
        st.subheader("Rutina de Entrenamiento")
        st.write(f"Plan para: {st.session_state.obj}")
        st.write("✅ Press Banca (4x10)\n✅ Sentadilla (4x10)\n✅ Remo (3x12)")

    elif st.session_state.page == "Supl":
        st.subheader("Suplementación")
        st.write("• Creatina: 5g al día\n• Proteína: 30g post-entreno")

    elif st.session_state.page == "Progreso":
        st.subheader("Progreso y Seguimiento")
        st.write("Registra tu peso semanal para ajustar la IA.")
        if st.number_input("Peso (kg)"): st.button("Guardar")

    elif st.session_state.page == "Chat":
        st.subheader("Asistente IA")
        st.text_input("¿Duda?")

    # --- MENÚ FIJO (Siempre abajo) ---
    st.markdown('<div class="fixed-menu">', unsafe_allow_html=True)
    cols = st.columns(4)
    if cols[0].button("💪"): st.session_state.page = "Entrenar"
    if cols[1].button("💊"): st.session_state.page = "Supl"
    if cols[2].button("📈"): st.session_state.page = "Progreso"
    if cols[3].button("💬"): st.session_state.page = "Chat"
    st.markdown('</div>', unsafe_allow_html=True)

