import streamlit as st
import pandas as pd
from datetime import date

def _init_state():
    if "compras" not in st.session_state:
        st.session_state["compras"] = pd.DataFrame(
            columns=["Fecha", "Proveedor", "Producto", "Cantidad", "Precio Unitario", "Total", "Método de pago", "Notas"]
        )

def mostrar_compras():
    st.title("📥 Compras")

    _init_state()

    with st.expander("➕ Registrar nueva compra", expanded=True):
        with st.form("form_compras", clear_on_submit=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                fecha = st.date_input("Fecha", value=date.today())
                proveedor = st.text_input("Proveedor")
            with col2:
                producto = st.text_input("Producto / Insumo")
                cantidad = st.number_input("Cantidad", min_value=0.0, step=1.0, format="%.2f")
            with col3:
                precio_unit = st.number_input("Precio unitario", min_value=0.0, step=0.01, format="%.2f")
                metodo = st.selectbox("Método de pago", ["Efectivo", "Tarjeta", "Transferencia", "Crédito a proveedor"])
            notas = st.text_area("Notas (opcional)", placeholder="Lote, condiciones, referencia de factura, etc.")

            submitted = st.form_submit_button("Guardar compra")
            if submitted:
                # Validaciones simples
                if not proveedor:
                    st.warning("Ingresa el nombre del proveedor.")
                elif not producto:
                    st.warning("Ingresa el nombre del producto/insumo.")
                elif cantidad <= 0:
                    st.warning("La cantidad debe ser mayor que 0.")
                elif precio_unit <= 0:
                    st.warning("El precio unitario debe ser mayor que 0.")
                else:
                    total = round(cantidad * precio_unit, 2)
                    nueva = {
                        "Fecha": pd.to_datetime(fecha),
                        "Proveedor": proveedor.strip(),
                        "Producto": producto.strip(),
                        "Cantidad": float(cantidad),
                        "Precio Unitario": float(precio_unit),
                        "Total": total,
                        "Método de pago": metodo,
                        "Notas": notas.strip(),
                    }
                    st.session_state["compras"] = pd.concat(
                        [st.session_state["compras"], pd.DataFrame([nueva])],
                        ignore_index=True
                    )
                    st.success(f"Compra registrada: {producto} por {total:,.2f}")

    # Tabla de compras
    st.subheader("📋 Historial de compras")
    if st.session_state["compras"].empty:
        st.info("Aún no hay compras registradas.")
    else:
        # Ordenar por fecha descendente
        df = st.session_state["compras"].sort_values("Fecha", ascending=False).reset_index(drop=True)
        st.dataframe(
            df.style.format({
                "Cantidad": "{:,.2f}",
                "Precio Unitario": "{:,.2f}",
                "Total": "{:,.2f}"
            }),
            use_container_width=True,
            hide_index=True
        )

        # Resumen
        st.subheader("🧾 Resumen")
        colA, colB, colC = st.columns(3)
        with colA:
            st.metric("Total gastado", f"{df['Total'].sum():,.2f}")
        with colB:
            st.metric("Ítems comprados", f"{int((df['Cantidad']).sum()):,}")
        with colC:
            st.metric("Órdenes de compra", f"{len(df):,}")

        # Filtros rápidos
        with st.expander("🔎 Filtros rápidos"):
            proveedores = ["(Todos)"] + sorted(df["Proveedor"].dropna().unique().tolist())
            prov_sel = st.selectbox("Proveedor", proveedores)
            metodo_sel = st.multiselect("Método de pago", df["Método de pago"].dropna().unique().tolist())

            dff = df.copy()
            if prov_sel != "(Todos)":
                dff = dff[dff["Proveedor"] == prov_sel]
            if metodo_sel:
                dff = dff[dff["Método de pago"].isin(metodo_sel)]

            st.dataframe(
                dff.style.format({
                    "Cantidad": "{:,.2f}",
                    "Precio Unitario": "{:,.2f}",
                    "Total": "{:,.2f}"
                }),
                use_container_width=True,
                hide_index=True
            )
