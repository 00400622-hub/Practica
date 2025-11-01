import streamlit as st
from modulos.config.conexion import obtener_conexion

def mostrar_venta():
    st.header("🛒 Registrar venta simple")

    try:
        con = obtener_conexion()
        cursor = con.cursor()

        # Formulario para registrar la venta
        with st.form("form_venta"):
            producto = st.text_input("Nombre del producto")
            cantidad = st.number_input("Cantidad", min_value=1, step=1)
            enviar = st.form_submit_button("✅ Guardar venta")

            if enviar:
                if producto.strip() == "":
                    st.warning("⚠️ Debes ingresar el nombre del producto.")
                else:
                    try:
                        cursor.execute(
                            "INSERT INTO Ventas (Producto, Cantidad) VALUES (%s, %s)",
                            (producto, str(cantidad))
                        )
                        con.commit()
                        st.success(f"✅ Venta registrada correctamente: {producto} (Cantidad: {cantidad})")
                        st.rerun()
                    except Exception as e:
                        con.rollback()
                        st.error(f"❌ Error al registrar la venta: {e}")

    except Exception as e:
        st.error(f"❌ Error general: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'con' in locals():
            con.close()
