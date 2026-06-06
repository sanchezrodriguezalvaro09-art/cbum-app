import streamlit as st
import sqlite3

# --- 1. CONFIGURACIÓN ELITE ---
st.set_page_config(page_title="CBum Elite Pro", layout="centered")
st.markdown("""
    <style>
    .stApp { background: #000000; color: #FFD700; }
    .fixed-menu { position: fixed; bottom: 0; left: 0; width: 100%; background: #0a0a0a; 
                  padding: 15px; display: flex; justify-content: space-around; 
                  border-top: 2px solid #0000FF; z-index: 999; }
    .stButton button { color: #FFD700; background-color: #111; border: 1px solid #0000FF; width: 100%; }
    h1, h2 { color: #FFD700 !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. BASE DE DATOS ---
conn = sqlite3.connect('cbum_elite_final_pro.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS usuarios 
             (id INTEGER PRIMARY KEY, nombre TEXT UNIQUE, pass TEXT, peso REAL, altura REAL, objetivo TEXT, dias INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS historial_peso (usuario TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, peso REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS historial_ejercicios (usuario TEXT, ejercicio TEXT, peso_kg REAL, reps INTEGER, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
c.execute('''CREATE TABLE IF NOT EXISTS diario_nutricion (usuario TEXT, fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP, calorias REAL, info TEXT)''')
conn.commit()

# --- 3. MOTOR IA ELITE ---
imagenes_ejercicios = {
    "Press Banca": "https://www.exercises.com.au/wp-content/uploads/2015/05/Barbell-bench-press_1.png",
    "Press Militar": "https://www.exercises.com.au/wp-content/uploads/2015/05/Standing-military-press_1.png",
    "Sentadilla": "https://www.exercises.com.au/wp-content/uploads/2015/05/Barbell-squat_1.png",
    "Dominadas": "https://www.exercises.com.au/wp-content/uploads/2015/05/Pull-up_1.png",
    "Remo": "https://www.exercises.com.au/wp-content/uploads/2015/05/Bent-over-row_1.png",
    "Curl": "https://www.exercises.com.au/wp-content/uploads/2015/05/Barbell-curl_1.png"
}

def generar_rutina_ia(obj, dias, historial_fuerza):
    variante = "Estándar"
    if len(historial_fuerza) >= 5:
        pesos = [h[1] for h in historial_fuerza[:5]]
        if all(x <= pesos[0] for x in pesos[1:]): variante = "Avanzada"
    rango = {"Hipertrofia": "4x10-12", "Fuerza": "5x3-5", "Músculo Magro": "3x10-15", "Definición": "4x15-20"}
    r = rango.get(obj, "3x12")
    
    if variante == "Avanzada":
        ejercicios_pro = {
            "Empuje": [f"Press Banca con Pausa {r}", f"Press Militar tras nuca {r}", f"Fondos en paralelas {r}", f"Extensiones polea {r}"],
            "Tracción": [f"Dominadas lastradas {r}", f"Remo Pendlay {r}", f"Curl Predicador {r}", f"Curl martillo {r}"],
            "Pierna": [f"Sentadilla Zercher {r}", f"Prensa unilateral {r}", f"Peso muerto rumano {r}", f"Gemelos donkey {r}"],
            "Torso": [f"Press declinado {r}", f"Remo a una mano {r}", f"Elevaciones laterales inclinado {r}", f"Abdominales colgado {r}"],
            "Fullbody": [f"Peso Muerto {r}", f"Press Banca {r}", f"Remo {r}", f"Press Militar {r}"]
        }
    else:
        ejercicios_pro = {
            "Empuje": [f"Press Banca {r}", f"Press Militar {r}", f"Aperturas {r}", f"Press Francés {r}"],
            "Tracción": [f"Dominadas {r}", f"Remo con Barra {r}", f"Curl con Barra {r}", f"Curl Inverso {r}"],
            "Pierna": [f"Sentadilla {r}", f"Prensa {r}", f"Curl Femoral {r}", f"Gemelos {r}", f"Crunch Abdomen {r}"],
            "Torso": [f"Press Inclinado {r}", f"Jalón al pecho {r}", f"Elevaciones Laterales {r}", f"Plancha {r}"],
            "Fullbody": [f"Peso Muerto {r}", f"Press Banca {r}", f"Remo {r}", f"Press Militar {r}"]
        }
    estructura = {3: ["Empuje", "Tracción", "Pierna"], 4: ["Torso", "Pierna", "Empuje", "Tracción"], 5: ["Empuje", "Tracción", "Pierna", "Torso", "Fullbody"]}
    plan = {}
    dias_sel = estructura.get(dias, estructura[3])
    for i, tipo in enumerate(dias_sel):
        plan[f"Día {i+1}: {tipo}"] = ejercicios_pro[tipo]
    return plan

# --- 4. GESTIÓN SESIÓN ---
if 'user' not in st.session_state: st.session_state.user = None

if not st.session_state.user:
    st.title("🚀 CBUM ELITE PRO")
    tab1, tab2 = st.tabs(["ENTRAR", "REGISTRO ELITE"])
    with tab2:
        with st.form("reg"):
            n, p = st.text_input("Usuario"), st.text_input("Contraseña", type="password")
            alt, pes = st.number_input("Altura"), st.number_input("Peso")
            obj = st.selectbox("Objetivo", ["Hipertrofia", "Fuerza", "Músculo Magro", "Definición"])
            dias = st.slider("Días", 3, 5, 4)
            if st.form_submit_button("Registrarse"):
                try:
                    c.execute("INSERT INTO usuarios (nombre, pass, peso, altura, objetivo, dias) VALUES (?,?,?,?,?,?)", (n, p, pes, alt, obj, dias))
                    conn.commit()
                    st.success("Registrado.")
                except: st.error("Usuario existe.")
    with tab1:
        with st.form("login"):
            un, up = st.text_input("User"), st.text_input("Pass", type="password")
            if st.form_submit_button("Acceder"):
                c.execute("SELECT * FROM usuarios WHERE nombre=? AND pass=?", (un, up))
                user = c.fetchone()
                if user:
                    st.session_state.user = user[1]
                    st.session_state.data = user
                    st.rerun()
else:
    if 'page' not in st.session_state: st.session_state.page = "Entrenar"
    
    st.markdown('<div class="fixed-menu">', unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    if c1.button("💪"): st.session_state.page = "Entrenar"
    if c2.button("💊"): st.session_state.page = "Supl"
    if c3.button("📈"): st.session_state.page = "Progreso"
    if c4.button("🥑"): st.session_state.page = "Nutricion"
    if c5.button("💬"): st.session_state.page = "Chat"
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.page == "Entrenar":
        c.execute("SELECT ejercicio, peso_kg, reps FROM historial_ejercicios WHERE usuario=?", (st.session_state.user,))
        historial = c.fetchall()
        st.subheader(f"Rutina Elite: {st.session_state.data[5]}")
        plan = generar_rutina_ia(st.session_state.data[5], st.session_state.data[6], historial)
        for dia, ejer in plan.items():
            with st.expander(dia):
                for e in ejer:
                    st.write(f"✅ {e}")
                    nombre_busqueda = "".join([i for i in e.split("4x")[0].split("5x")[0].split("3x")[0] if i.isalpha() or i == " "]).strip()
                    for clave in imagenes_ejercicios:
                        if clave.lower() in nombre_busqueda.lower():
                            st.image(imagenes_ejercicios[clave], width=200)
                            break
    
    elif st.session_state.page == "Supl":
        st.subheader("Plan de Suplementación Elite")
        peso, obj = st.session_state.data[3], st.session_state.data[5]
        suplementos = {"Creatina": f"{round(peso * 0.05, 1)}g/día", "Proteína": f"{round(peso * 1.8, 0)}g/día"}
        for n, d in suplementos.items():
            with st.expander(f"💊 {n}"): st.write(d)
    
    elif st.session_state.page == "Nutricion":
        st.subheader("🥑 Registro Nutricional IA")
        foto = st.file_uploader("Sube foto de tu comida", type=["jpg", "png"])
        if foto:
            st.image(foto, caption="Analizando plato...")
            st.info("IA: Estimando macronutrientes... (Modo Demo: Tu plato contiene aprox 500 kcal).")
            if st.button("Guardar en diario"):
                c.execute("INSERT INTO diario_nutricion (usuario, calorias, info) VALUES (?, ?, ?)", (st.session_state.user, 500, "Plato analizado"))
                conn.commit()
                st.success("Registrado en tu historial.")

    elif st.session_state.page == "Progreso":
        st.subheader("📊 Seguimiento")
        nuevo_peso = st.number_input("Peso actual", value=float(st.session_state.data[3]))
        if st.button("Guardar"):
            c.execute("INSERT INTO historial_peso (usuario, peso) VALUES (?, ?)", (st.session_state.user, nuevo_peso))
            conn.commit()
        st.divider()
        with st.form("carga"):
            ejer = st.text_input("Ejercicio")
            kilos = st.number_input("Kilos")
            reps = st.number_input("Reps")
            if st.form_submit_button("Registrar"):
                c.execute("INSERT INTO historial_ejercicios (usuario, ejercicio, peso_kg, reps) VALUES (?, ?, ?, ?)", (st.session_state.user, ejer, kilos, reps))
                conn.commit()
                st.rerun()

    elif st.session_state.page == "Chat":
        st.subheader("IA Coach")
        q = st.text_input("Pregunta al Coach:")
        if q: st.write("IA: Si no progresas, tu cuerpo pide un nuevo estímulo.")
