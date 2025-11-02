import streamlit as st
from modulos.config.conexion import obtener_conexion

def mostrar_clientes():
    st.header("👥 Registro de Clientes")

    try:
        con = obtener_conexion()
        cursor = con.cursor()

        # Formulario para registrar un cliente
        with st.form("form_clientes"):
            nombre = st.text_input("Nombre del cliente")
            correo = st.text_input("Correo electrónico")
            enviar = st.form_submit_button("✅ Guardar cliente")

            if enviar:
                if nombre.strip() == "" or correo.strip() == "":
                    st.warning("⚠️ Debes ingresar nombre y correo.")
                else:
                    try:
                        cursor.execute(
                            "INSERT INTO Clientes (Nombre, Correo) VALUES (%s, %s)",
                            (nombre, correo)
                        )
                        con.commit()
                        st.success(f"✅ Cliente registrado: {nombre}")
                        st.rerun()
                    except Exception as e:
                        con.rollback()
                        st.error(f"❌ Error al registrar el cliente: {e}")

    except Exception as e:
        st.error(f"❌ Error general: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()
