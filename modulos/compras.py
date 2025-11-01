import streamlit as st
import mysql.connector

# Conexión con tu base de datos de Clever Cloud
def get_connection():
    return mysql.connector.connect(
        host="bxu2mxxxxx-mysql.services.clever-cloud.com",  # tu host de Clever Cloud
        user="tu_usuario",       # tu usuario
        password="tu_contraseña",# tu contraseña
        database="buap2lwlapikiigfik04",
        port=3306
    )

def mostrar_compras():
    st.title("🛒 Registro de Compras")

    producto = st.text_input("Producto")
    cantidad = st.text_input("Cantidad")

    if st.button("Guardar compra"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO Compras (Producto, Cantidad)
                VALUES (%s, %s)
            """, (producto, cantidad))
            conn.commit()
            cur.close()
            conn.close()
            st.success("✅ Compra registrada correctamente.")
        except Exception as e:
            st.error(f"Error al guardar la compra: {e}")

    if st.button("Mostrar compras"):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM Compras ORDER BY Id_Compra DESC")
            datos = cur.fetchall()
            conn.close()

            if datos:
                st.subheader("📋 Compras registradas")
                st.table(datos)
            else:
                st.info("No hay compras registradas.")
        except Exception as e:
            st.error(f"Error al cargar las compras: {e}")
