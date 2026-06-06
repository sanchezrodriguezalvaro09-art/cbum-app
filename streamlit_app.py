import streamlit as st
import sqlite3
import datetime

st.set_page_config(page_title="CBum Elite Training", layout="centered")

# --- Base de Datos ---
conn = sqlite3.connect('fitness_elite.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios (nombre TEXT PRIMARY KEY, peso REAL, altura REAL, objetivo TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS progreso (usuario TEXT, fecha TEXT, ejercicio TEXT, peso REAL)''')
conn.commit()

# --- Gestión de Sesión ---
if 'user' not in st.session_state: st.session_state.user = None

if st.session_state.user is None:
    st.title("CBUM ELITE TRAINING")
    # ... (Mantén tu lógica de Login/Registro aquí) ...
    nombre = st.text_input("Usuario")
    if st.button("Iniciar Sesión"):
        st.session_state.user = nombre
        st.rerun()
else:
    st.title(f"Bienvenido, {st.session_state.user} 👋")
    
    # --- Menú Inferior ---
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("💪 Entrenar"): st.session_state.page = "Entrenar"
    if c2.button("💊 Supl."): st.session_state.page = "Supl"
    if c3.button("📈 Evolución"): st.session_state.page = "Evolución"
    if c4.button("💬 Chat AI"): st.session_state.page = "Chat"
    
    page = st.session_state.get("page", "Entrenar")

    if page == "Entrenar":
        st.subheader("Rutina de Entrenamiento")
        ejercicio = st.selectbox("Elige ejercicio:", ["Press Banca", "Sentadilla", "Remo"])
        peso = st.number_input("Peso levantado (kg):", 0.0, 300.0)
        if st.button("Registrar Peso"):
            c.execute("INSERT INTO progreso VALUES (?,?,?,?)", (st.session_state.user, str(datetime.date.today()), ejercicio, peso))
            conn.commit()
            st.success("¡Peso guardado!")
        st.write("---")
        # Aquí puedes poner tu temporizador
        if st.button("⏱️ Iniciar descanso (90s)"): st.write("Descansando...")

    elif page == "Supl":
        st.subheader("Tu Suplementación")
        st.write("- Creatina: 5g al día")
        st.write("- Proteína: 1 scoop post-entreno")
        st.write("- Omega 3: 2 cápsulas")

    elif page == "Evolución":
        st.subheader("Tabla de Progreso")
        datos = c.execute("SELECT * FROM progreso WHERE usuario=?", (st.session_state.user,)).fetchall()
        st.table(datos)
        
        st.write("---")
        nuevo_peso = st.number_input("Peso corporal actual (kg):")
        if st.button("Actualizar peso corporal"):
            st.success(f"Peso {nuevo_peso}kg guardado. Ajustando rutina...")

