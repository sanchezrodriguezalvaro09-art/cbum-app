import streamlit as st
import sqlite3
import datetime

st.set_page_config(page_title="CBum Elite Training", layout="centered")

# --- CSS para Menú Fijo Inferior ---
st.markdown("""
    <style>
    .fixed-menu {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f0f2f6;
        padding: 10px;
        display: flex;
        justify-content: space-around;
        border-top: 2px solid #ddd;
        z-index: 999;
    }
    </style>
""", unsafe_allow_html=True)

# --- Base de Datos ---
conn = sqlite3.connect('fitness_elite.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (nombre TEXT PRIMARY KEY, peso REAL, altura REAL, objetivo TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS progreso (usuario TEXT, fecha TEXT, ejercicio TEXT, peso REAL)''')
conn.commit()

# --- Gestión de Sesión ---
if 'user' not in st.session_state: st.session_state.user = None
if 'page' not in st.session_state: st.session_state.page = "Entrenar"

# --- Menú Inferior (HTML Fijo) ---
st.markdown('<div class="fixed-menu">', unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
if col1.button("💪"): st.session_state.page = "Entrenar"
if col2.button("💊"): st.session_state.page = "Supl"
if col3.button("📈"): st.session_state.page = "Evolución"
if col4.button("💬"): st.session_state.page = "Chat"
st.markdown('</div>', unsafe_allow_html=True)

# --- Lógica de Contenido ---
if st.session_state.page == "Entrenar":
    st.subheader("Rutina de Entrenamiento")
    ejercicio = st.selectbox("Elige ejercicio:", ["Press Banca", "Sentadilla", "Remo"])
    peso = st.number_input("Peso levantado (kg):", 0.0, 300.0)
    if st.button("Registrar Peso"):
        c.execute("INSERT INTO progreso VALUES (?,?,?,?)", (st.session_state.user, str(datetime.date.today()), ejercicio, peso))
        conn.commit()
    st.write("Temporizador, rutinas y ejercicios aquí...")

elif st.session_state.page == "Supl":
    st.subheader("Tu Suplementación")
    st.write("Lista de suplementos según tu objetivo:")
    st.info("Creatina: 5g | Proteína: 1 scoop | Omega 3: 2 cap.")

elif st.session_state.page == "Evolución":
    st.subheader("Tabla de Evolución")
    datos = c.execute("SELECT * FROM progreso WHERE usuario=?", (st.session_state.user,)).fetchall()
    st.table(datos)
    peso_actual = st.number_input("Actualizar peso corporal (kg):")

elif st.session_state.page == "Chat":
    st.subheader("Chat de Ayuda")
    st.write("Pregunta cualquier duda sobre tu rutina.")

