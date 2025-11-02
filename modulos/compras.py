import streamlit as st
from modulos.config.conexion import obtener_conexion

def mostrar_compras():
    st.header("🛍️ Registro de Compras")

    try:
        con = obtener_conexion()
        cursor = con.cursor()

        # Formulario para registrar la compra
        with st.form("form_compras"):
            producto = st.text_input("Producto")
            cantidad = st.number_input("Cantidad", min_value=1, step=1)
            enviar = st.form_submit_button("✅ Guardar compra")

            if enviar:
                if producto.strip() == "":
                    st.warning("⚠️ Debes ingresar el nombre del producto.")
                else:
                    try:
                        # Nota: Cantidad es VARCHAR(100) en la tabla, por eso se convierte a str
                        cursor.execute(
                            "INSERT INTO Compras (Producto, Cantidad) VALUES (%s, %s)",
                            (producto, str(cantidad))
                        )
                        con.commit()
                        st.success(f"✅ Compra registrada: {producto} (Cantidad: {cantidad})")
                        st.rerun()
                    except Exception as e:
                        con.rollback()
                        st.error(f"❌ Error al registrar la compra: {e}")

    except Exception as e:
        st.error(f"❌ Error general: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()
