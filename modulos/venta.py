import streamlit as st
import pandas as pd
from modulos.config.conexion import obtener_conexion

def mostrar_venta():
    st.header("🛒 Registrar venta simple")

    # ---------- INSERT ----------
    try:
        con = obtener_conexion()
        cursor = con.cursor()

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
                            (producto, str(cantidad))  # Cantidad es VARCHAR en tu BD
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
        if 'cursor' in locals(): cursor.close()
        if 'con' in locals(): con.close()

    # ---------- LISTAR / EDITAR / ELIMINAR ----------
    st.subheader("📋 Ventas registradas")
    try:
        con = obtener_conexion()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM Ventas ORDER BY Id_Venta DESC")
        rows = cur.fetchall()
        cur.close()
        con.close()

        if not rows:
            st.info("No hay ventas registradas.")
            return

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        ids = [r["Id_Venta"] for r in rows]
        sel = st.selectbox("Selecciona el Id_Venta para editar/eliminar", ids)

        if sel:
            row = next(r for r in rows if r["Id_Venta"] == sel)
            with st.form("form_editar_venta"):
                nuevo_producto = st.text_input("Producto", value=row["Producto"])
                nueva_cantidad = st.text_input("Cantidad", value=row["Cantidad"])  # VARCHAR

                col1, col2 = st.columns(2)
                actualizar = col1.form_submit_button("💾 Actualizar")
                eliminar = col2.form_submit_button("🗑️ Eliminar")

                if actualizar:
                    try:
                        con = obtener_conexion()
                        cur = con.cursor()
                        cur.execute(
                            "UPDATE Ventas SET Producto=%s, Cantidad=%s WHERE Id_Venta=%s",
                            (nuevo_producto, nueva_cantidad, sel)
                        )
                        con.commit()
                        cur.close(); con.close()
                        st.success("✅ Venta actualizada.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al actualizar: {e}")

                if eliminar:
                    try:
                        con = obtener_conexion()
                        cur = con.cursor()
                        cur.execute("DELETE FROM Ventas WHERE Id_Venta=%s", (sel,))
                        con.commit()
                        cur.close(); con.close()
                        st.success("🗑️ Venta eliminada.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al eliminar: {e}")
    except Exception as e:
        st.error(f"Error al listar/operar ventas: {e}")

