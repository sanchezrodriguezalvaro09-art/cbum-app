import streamlit as st
import sqlite3
import datetime

st.set_page_config(page_title="CBum Elite Training", layout="centered")

# --- Base de Datos ---
conn = sqlite3.connect('fitness_elite.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
             (nombre TEXT PRIMARY KEY, password TEXT, peso_inicial REAL, altura REAL, objetivo TEXT, dias_entreno INTEGER, peso_meta REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS progreso_semanal (usuario TEXT, fecha TEXT, peso_actual REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS registros_ejercicios (usuario TEXT, fecha TEXT, ejercicio TEXT, peso REAL)''')
conn.commit()

# --- Gestión de Sesión ---
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
        altura = st.number_input("Altura (cm)", 140, 220, 175)
        dias = st.slider("Días de entreno por semana", 3, 6, 4)
        obj = st.selectbox("Objetivo", ["Hipertrofia/Volumen", "Fuerza Pura", "Músculo Magro", "Definición"])
        meta = st.number_input("Peso objetivo (kg)", 40.0, 150.0, 75.0)
        
        if st.button("Registrarse"):
            try:
                c.execute("INSERT INTO usuarios VALUES (?,?,?,?,?,?,?)", (n, p, peso, altura, obj, dias, meta))
                conn.commit()
                st.success("Registrado. Ve a Iniciar Sesión.")
            except:
                st.error("El usuario ya existe.")
    
    with tab1:
        u = st.text_input("Usuario", key="un")
        pw = st.text_input("Contraseña", type="password", key="up")
        if st.button("Entrar"):
            c.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?", (u, pw))
            if c.fetchone():
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Credenciales incorrectas.")

# --- APP PRINCIPAL ---
else:
    st.title(f"Bienvenido, {st.session_state.user}")
    
    # Menú (Columnas para navegación)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("💪 Entrenar"): st.session_state.page = "Entrenar"
    if c2.button("💊 Supl."): st.session_state.page = "Supl"
    if c3.button("📈 Progreso"): st.session_state.page = "Progreso"
    if c4.button("💬 Chat AI"): st.session_state.page = "Chat"

    st.markdown("---")

    if st.session_state.page == "Entrenar":
        st.subheader("Rutina de Entrenamiento")
        ej = st.text_input("Ejercicio realizado")
        kg = st.number_input("Peso levantado (kg)")
        if st.button("Guardar registro"):
            c.execute("INSERT INTO registros_ejercicios VALUES (?,?,?,?)", (st.session_state.user, str(datetime.date.today()), ej, kg))
            conn.commit()
            st.success("Guardado.")

    elif st.session_state.page == "Supl":
        st.subheader("Suplementación")
        st.write("• Creatina: 5g | Proteína: 1 scoop")
        if st.button("Desactivar avisos hasta mañana"):
            st.success("Avisos desactivados.")

    elif st.session_state.page == "Progreso":
        st.subheader("Tu Evolución")
        peso_actual = st.number_input("Peso actual (kg)")
        if st.button("Registrar peso semanal"):
            c.execute("INSERT INTO progreso_semanal VALUES (?,?,?)", (st.session_state.user, str(datetime.date.today()), peso_actual))
            conn.commit()
            st.success("Progreso guardado.")

    elif st.session_state.page == "Chat":
        st.subheader("Asistente IA")
        q = st.text_input("¿Qué duda tienes?")
        if q:
            st.write("🤖 IA: Analizando tus datos...")

