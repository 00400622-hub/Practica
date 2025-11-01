# app.py
import streamlit as st
from modulos.venta import mostrar_venta  # Importamos la función mostrar_venta del módulo venta
from modulos.login import login
from modulos.compras import mostrar_compras

# Comprobamos si la sesión ya está iniciada
if "sesion_iniciada" in st.session_state and st.session_state["sesion_iniciada"]:
    # Si la sesión está iniciada, mostrar el contenido de ventas o menú principal
    opciones = ["Ventas", "Otra opción"]  # Agrega más opciones si las necesitas
    seleccion = st.sidebar.selectbox("Selecciona una opción", opciones)

    if seleccion == "Ventas":
        mostrar_venta()
    elif seleccion == "Otra opción":
        st.write("Has seleccionado otra opción.")
else:
    # Si la sesión no está iniciada, mostrar el login
    login()
