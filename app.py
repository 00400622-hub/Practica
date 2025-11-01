import streamlit as st
from modulos.venta import mostrar_venta
from modulos.login import login
from modulos.compras import mostrar_compras

if "sesion_iniciada" in st.session_state and st.session_state["sesion_iniciada"]:
    seleccion = st.sidebar.selectbox("Selecciona una opción", ["Ventas", "Compras", "Otra opción"])

    if seleccion == "Ventas":
        mostrar_venta()          # <-- SOLO Ventas aquí
    elif seleccion == "Compras":
        mostrar_compras()        # <-- SOLO Compras aquí
    else:
        st.write("Has seleccionado otra opción.")
else:
    login()
