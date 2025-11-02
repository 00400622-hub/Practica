import streamlit as st
import pandas as pd
from modulos.config.conexion import obtener_conexion

def mostrar_compras():
    st.header("🛍️ Registro de Compras")

    # ---------- INSERT ----------
    try:
        con = obtener_conexion()
        cursor = con.cursor()

        with st.form("form_compras"):
            producto = st.text_input("Producto")
            cantidad = st.number_input("Cantidad", min_value=1, step=1)
            enviar = st.form_submit_button("✅ Guardar compra")

            if enviar:
                if producto.strip() == "":
                    st.warning("⚠️ Debes ingresar el nombre del producto.")
                else:
                    try:
                        cursor.execute(
                            "INSERT INTO Compras (Producto, Cantidad) VALUES (%s, %s)",
                            (producto, str(cantidad))  # Cantidad VARCHAR
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
        if 'cursor' in locals(): cursor.close()
        if 'con' in locals(): con.close()

    # ---------- LISTAR / EDITAR / ELIMINAR ----------
    st.subheader("📋 Compras registradas")
    try:
        con = obtener_conexion()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM Compras ORDER BY Id_Compra DESC")
        rows = cur.fetchall()
        cur.close()
        con.close()

        if not rows:
            st.info("No hay compras registradas.")
            return

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        ids = [r["Id_Compra"] for r in rows]
        sel = st.selectbox("Selecciona el Id_Compra para editar/eliminar", ids)

        if sel:
            row = next(r for r in rows if r["Id_Compra"] == sel)
            with st.form("form_editar_compra"):
                nuevo_producto = st.text_input("Producto", value=row["Producto"])
                nueva_cantidad = st.text_input("Cantidad", value=row["Cantidad"])

                col1, col2 = st.columns(2)
                actualizar = col1.form_submit_button("💾 Actualizar")
                eliminar = col2.form_submit_button("🗑️ Eliminar")

                if actualizar:
                    try:
                        con = obtener_conexion()
                        cur = con.cursor()
                        cur.execute(
                            "UPDATE Compras SET Producto=%s, Cantidad=%s WHERE Id_Compra=%s",
                            (nuevo_producto, nueva_cantidad, sel)
                        )
                        con.commit()
                        cur.close(); con.close()
                        st.success("✅ Compra actualizada.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al actualizar: {e}")

                if eliminar:
                    try:
                        con = obtener_conexion()
                        cur = con.cursor()
                        cur.execute("DELETE FROM Compras WHERE Id_Compra=%s", (sel,))
                        con.commit()
                        cur.close(); con.close()
                        st.success("🗑️ Compra eliminada.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al eliminar: {e}")
    except Exception as e:
        st.error(f"Error al listar/operar compras: {e}")

