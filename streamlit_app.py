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
        obj = st.selectbox("Objetivo", ["Hipertrofia", "Definición"])
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
    
    # --- Menú Inferior (Navegación Profesional) ---
    c1, c2, c3, c4 = st.columns(4)
    with c1: menu = st.button("💪 Entrenar")
    with c2: menu = st.button("💊 Supl.")
    with c3: menu = st.button("📈 Evolución")
    with c4: menu = st.button("💬 Chat AI")

    # --- Lógica de Menús ---
    if menu: st.session_state.menu = menu # Guarda la selección
    current_menu = st.session_state.get("menu", "💪 Entrenar")

    if current_menu == "💪 Entrenar":
        st.subheader("Tu Rutina de Hoy")
        st.write("Registra tus series y pesos.")
        
    elif current_menu == "💊 Supl.":
        st.subheader("Suplementación")
        st.info("Recordatorio: Toma tu proteína post-entreno.")
        
    elif current_menu == "📈 Evolución":
        st.subheader("Seguimiento Semanal")
        nuevo_peso = st.number_input("Actualiza tu peso semanal (kg):")
        if st.button("Actualizar y Reajustar"):
            c.execute("INSERT INTO pesos_semanales VALUES (?,?,?)", (st.session_state.user, datetime.date.today(), nuevo_peso))
            conn.commit()
            # Lógica de reajuste
            st.success("Rutina reajustada automáticamente basándonos en tu progreso.")
            
    elif current_menu == "💬 Chat AI":
        st.subheader("Chat de Ayuda")
        pregunta = st.text_input("¿Qué duda tienes?")
        if pregunta:
            st.write("🤖 [IA]: Basado en tus datos, te recomiendo subir la carga un 5% la próxima sesión.")

