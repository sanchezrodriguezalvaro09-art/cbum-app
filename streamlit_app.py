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
conn.commit()

# --- 3. MOTOR IA ELITE ---
def generar_rutina_ia(obj, dias):
    rango = {"Hipertrofia": "4x10-12", "Fuerza": "5x3-5", "Músculo Magro": "3x10-15", "Definición": "4x15-20"}
    r = rango.get(obj, "3x12")
    ejercicios_pro = {
        "Empuje": [f"Press Banca {r}", f"Press Militar {r}", f"Aperturas {r}", f"Press Francés {r}"],
        "Tracción": [f"Dominadas {r}", f"Remo con Barra {r}", f"Curl con Barra {r}", f"Curl Inverso (Antebrazo) {r}"],
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
                    st.success("Registrado. ¡Entra ahora!")
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
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("💪"): st.session_state.page = "Entrenar"
    if c2.button("💊"): st.session_state.page = "Supl"
    if c3.button("📈"): st.session_state.page = "Progreso"
    if c4.button("💬"): st.session_state.page = "Chat"
    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.page == "Entrenar":
        st.subheader(f"Rutina Elite: {st.session_state.data[5]}")
        plan = generar_rutina_ia(st.session_state.data[5], st.session_state.data[6])
        for dia, ejer in plan.items():
            with st.expander(dia):
                for e in ejer: st.write(f"✅ {e}")
    
    elif st.session_state.page == "Supl":
        st.subheader("Plan de Suplementación Elite")
        peso, obj = st.session_state.data[3], st.session_state.data[5]
        # Cálculos precisos
        crea_total = round(peso * 0.05, 1)
        prot_total = round(peso * 1.8, 0)
        
        suplementos = {
            "Creatina Monohidrato": f"Dosis: {crea_total}g al día. Tomar una sola vez al día (Post-entreno o desayuno).",
            "Proteína Whey": f"Total diario: {prot_total}g de proteína. Tomar 1 o 2 batidos al día dependiendo de tu dieta sólida (Máx. 30g por batido).",
            "Omega-3 (EPA/DHA)": "Dosis: 2-3g al día repartidos en 2 tomas con las comidas principales.",
            "Magnesio (Bisglicinato)": "Dosis: 300mg al día. Tomar una sola toma antes de dormir."
        }
        if obj == "Definición": suplementos["Multivitamínico"] = "Dosis: 1 cápsula al día con el desayuno."
        if obj == "Fuerza": suplementos["Beta-Alanina"] = "Dosis: 3g al día repartidos en 2 tomas."
        
        for nombre, desc in suplementos.items():
            with st.expander(f"💊 {nombre}"): st.write(desc)
        st.warning("⚠️ Consulta siempre con tu médico.")
    
    elif st.session_state.page == "Progreso":
        st.subheader("Tu Evolución")
    
    elif st.session_state.page == "Chat":
        st.subheader("IA Coach")
        q = st.text_input("Pregunta al Coach:")
        if q: st.write("IA: Basado en tus datos, mantén la intensidad y controla la fase excéntrica.")

