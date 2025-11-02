import streamlit as st
import pandas as pd
from modulos.config.conexion import obtener_conexion

def mostrar_clientes():
    st.header("👥 Registro de Clientes")

    # ---------- INSERT ----------
    try:
        con = obtener_conexion()
        cursor = con.cursor()

        with st.form("form_clientes"):
            nombre = st.text_input("Nombre")
            correo = st.text_input("Correo")
            enviar = st.form_submit_button("✅ Guardar cliente")

            if enviar:
                if not nombre.strip() or not correo.strip():
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
        if 'cursor' in locals(): cursor.close()
        if 'con' in locals(): con.close()

    # ---------- LISTAR / EDITAR / ELIMINAR ----------
    st.subheader("📋 Clientes registrados")
    try:
        con = obtener_conexion()
        cur = con.cursor(dictionary=True)
        cur.execute("SELECT * FROM Clientes ORDER BY Id_Cliente DESC")
        rows = cur.fetchall()
        cur.close()
        con.close()

        if not rows:
            st.info("No hay clientes.")
            return

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        ids = [r["Id_Cliente"] for r in rows]
        sel = st.selectbox("Selecciona el Id_Cliente para editar/eliminar", ids)

        if sel:
            row = next(r for r in rows if r["Id_Cliente"] == sel)
            with st.form("form_editar_cliente"):
                nuevo_nombre = st.text_input("Nombre", value=row["Nombre"])
                nuevo_correo = st.text_input("Correo", value=row["Correo"])

                col1, col2 = st.columns(2)
                actualizar = col1.form_submit_button("💾 Actualizar")
                eliminar = col2.form_submit_button("🗑️ Eliminar")

                if actualizar:
                    try:
                        con = obtener_conexion()
                        cur = con.cursor()
                        cur.execute(
                            "UPDATE Clientes SET Nombre=%s, Correo=%s WHERE Id_Cliente=%s",
                            (nuevo_nombre, nuevo_correo, sel)
                        )
                        con.commit()
                        cur.close(); con.close()
                        st.success("✅ Cliente actualizado.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al actualizar: {e}")

                if eliminar:
                    try:
                        con = obtener_conexion()
                        cur = con.cursor()
                        cur.execute("DELETE FROM Clientes WHERE Id_Cliente=%s", (sel,))
                        con.commit()
                        cur.close(); con.close()
                        st.success("🗑️ Cliente eliminado.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al eliminar: {e}")
    except Exception as e:
        st.error(f"Error al listar/operar clientes: {e}")

