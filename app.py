import streamlit as st

JOULES_POR_PASO = 3
META_PASOS = 7500
DESCUENTO = 2


def calcular_energia(pasos):
    return pasos * JOULES_POR_PASO


def mostrar_resultados(pasos):
    energia = calcular_energia(pasos)
    st.write("Pasos:", pasos)
    st.write("Energía:", energia, "joules")
    st.write("Energía en kWh:", round(energia / 3600000, 6))


def entrar():
    with st.form("entrada"):
        nombre = st.text_input("Nombre del perfil de prueba")
        ingresar = st.form_submit_button("Entrar")

    if ingresar:
        nombre = nombre.strip().lower()
        if nombre:
            st.session_state.usuario = nombre
            if nombre not in st.session_state.perfiles:
                st.session_state.perfiles[nombre] = 0
            st.rerun()
        else:
            st.error("Escribe un nombre.")


def mostrar_cuenta():
    usuario = st.session_state.usuario
    st.write("Hola,", usuario)

    with st.form("pasos", clear_on_submit=True):
        nuevos_pasos = st.number_input("Añadir pasos de prueba", min_value=0, value=0, step=100)
        guardar = st.form_submit_button("Guardar pasos")

    if guardar:
        st.session_state.perfiles[usuario] += nuevos_pasos

    pasos = st.session_state.perfiles[usuario]
    mostrar_resultados(pasos)

    if pasos >= META_PASOS:
        st.success(f"Alcanzaste la meta: descuento propuesto del {DESCUENTO} % en la mensualidad.")
    else:
        st.write("Pasos que faltan para el descuento:", META_PASOS - pasos)

    if st.button("Salir"):
        st.session_state.usuario = ""
        st.rerun()


st.set_page_config(page_title="StepPower")
st.title("StepPower")
st.write("Cada paso equivale a 3 joules en este cálculo.")

if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "perfiles" not in st.session_state:
    st.session_state.perfiles = {}

calculadora, cuenta = st.tabs(["Calculadora", "Mi cuenta"])

with calculadora:
    pasos = st.number_input("Número de pasos", min_value=0, value=1000, step=100)
    mostrar_resultados(pasos)

with cuenta:
    st.caption("Perfil de prueba sin contraseña. Usa un nombre ficticio. Los pasos se ingresan manualmente y solo se guardan en esta sesión del navegador.")
    st.write(f"Meta: {META_PASOS} pasos para un descuento propuesto del {DESCUENTO} % en la mensualidad.")
    if st.session_state.usuario:
        mostrar_cuenta()
    else:
        entrar()
    st.caption("El descuento requiere aprobación de la universidad. Todavía no hay sensores conectados.")
