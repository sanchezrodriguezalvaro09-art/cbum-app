import streamlit as st
import sqlite3
import datetime

# --- Configuración de la App ---
st.set_page_config(page_title="CBum Elite Training", layout="centered")

# --- Base de Datos ---
conn = sqlite3.connect('fitness_elite.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
             (nombre TEXT PRIMARY KEY, password TEXT, peso REAL, altura REAL, objetivo TEXT, fecha_registro TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS pesos_semanales 
             (usuario TEXT, fecha TEXT, peso REAL)''')
conn.commit()

# --- Gestión de Sesión ---
if 'user' not in st.session_state: st.session_state.user = None

# --- Pantalla de Registro/Login ---
if st.session_state.user is None:
    st.title("CBUM ELITE TRAINING")
    tab1, tab2 = st.tabs(["Iniciar Sesión", "Registrarse"])
    
    with tab2:
        nombre = st.text_input("Nombre de usuario", key="reg_n")
        pwd = st.text_input("Contraseña", type="password", key="reg_p")
        peso = st.number_input("Peso inicial (kg)", 40.0, 150.0, 70.0)
        altura = st.number_input("Altura (cm)", 140, 220, 175)
        # --- NUEVOS OBJETIVOS ---
        obj = st.selectbox("Objetivo", [
            "Hipertrofia/Volumen", 
            "Fuerza Pura", 
            "Músculo Magro (Lean Bulk)", 
            "Definición"
        ])
        if st.button("Registrarse"):
            c.execute("INSERT INTO usuarios VALUES (?,?,?,?,?,?)", (nombre, pwd, peso, altura, obj, datetime.date.today()))
            conn.commit()
            st.success("Cuenta creada. Ve a 'Iniciar Sesión'.")

    with tab1:
        user_login = st.text_input("Usuario")
        pass_login = st.text_input("Contraseña", type="password")
        if st.button("Entrar"):
            c.execute("SELECT * FROM usuarios WHERE nombre=? AND password=?", (user_login, pass_login))
            if c.fetchone():
                st.session_state.user = user_login
                st.rerun()
            else: st.error("Credenciales incorrectas.")

# --- App Principal ---
else:
    st.title(f"Bienvenido, {st.session_state.user} 👋")
    
    # --- Menú Inferior (Navegación) ---
    c1, c2, c3, c4 = st.columns(4)
    with c1: btn_ent = st.button("💪 Entrenar")
    with c2: btn_sup = st.button("💊 Supl.")
    with c3: btn_evo = st.button("📈 Evolución")
    with c4: btn_chat = st.button("💬 Chat AI")

    # Lógica de navegación
    if btn_ent: st.session_state.page = "Entrenar"
    if btn_sup: st.session_state.page = "Supl"
    if btn_evo: st.session_state.page = "Evolución"
    if btn_chat: st.session_state.page = "Chat"
    
    page = st.session_state.get("page", "Entrenar")

    if page == "Entrenar":
        st.subheader("Tu Rutina de Hoy")
        st.write("Selecciona tu estilo de entrenamiento abajo.")
        # Aquí iría tu lógica de ejercicios
        
    elif page == "Supl":
        st.subheader("Suplementación")
        st.info("Recordatorio: Optimiza tu ingesta según tu objetivo seleccionado.")
        
    elif page == "Evolución":
        st.subheader("Seguimiento Semanal")
        nuevo_peso = st.number_input("Introduce tu peso actual para reajuste:", min_value=30.0, step=0.1)
        if st.button("Reajustar Rutina"):
            c.execute("INSERT INTO pesos_semanales VALUES (?,?,?)", (st.session_state.user, datetime.date.today(), nuevo_peso))
            conn.commit()
            st.success("Progreso registrado. Plan ajustado automáticamente.")
            
    elif page == "Chat":
        st.subheader("Chat de Ayuda")
        pregunta = st.text_input("¿Qué duda tienes?")
        if pregunta:
            st.write("🤖 [IA]: Analizando tu progreso... Ajustando volumen de entrenamiento.")

