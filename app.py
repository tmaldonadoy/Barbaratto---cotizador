import json
import os
import copy
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# ─────────────────────────────────────────────
#  CONFIGURACIÓN PERSISTENTE
# ─────────────────────────────────────────────

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


def cargar_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)


# ─────────────────────────────────────────────
#  LÓGICA DE NEGOCIO
# ─────────────────────────────────────────────

def _calcular_m2(largo, ancho, alto):
    m1 = ancho + alto + 50
    if m1 < 300:
        m1 = 300
    m11 = (largo + ancho) * 2 + 80
    if 1690 < m11 < 1900:
        m11 = 1900
    return m11 * m1 / 1_000_000


def _aplicar_bracket(costo, brackets):
    for b in brackets:
        if b["costo_min"] < costo <= b["costo_max"] or (b["costo_min"] == 0 and 0 < costo < b["costo_max"]):
            if b["tipo"] == "suma":
                precio = costo + b["valor"]
            else:
                precio = costo * b["valor"]
            return precio, b["cantidad_minima"], b["valor"], b["tipo"]
    return None, None, None, None


def cotizar_caja(cfg, tipo, largo, ancho, alto, con_impresion=False, caras=2):
    # STOCK
    if tipo == "12c":
        key = f"{largo}x{ancho}x{alto}"
        stock_precio = cfg["stock_12c"].get(key)
        if stock_precio is not None:
            return {"precio": stock_precio, "stock": True, "nombre": key, "cantidad_minima": None}

    m2 = _calcular_m2(largo, ancho, alto)
    costo = m2 * cfg["materiales"][tipo]

    if con_impresion:
        imp_key = f"{caras}_caras"
        costo += cfg["impresion"].get(imp_key, 0)

    precio, cant, valor_bracket, tipo_bracket = _aplicar_bracket(costo, cfg["brackets"][tipo])
    if precio is None:
        return {"error": True}

    margen_pct = ((precio - costo) / costo * 100) if costo > 0 else 0
    return {
        "precio": precio,
        "stock": False,
        "cantidad_minima": cant,
        "costo_base": costo,
        "m2": m2,
        "margen_pct": margen_pct,
    }


# ─────────────────────────────────────────────
#  STREAMLIT CONFIG
# ─────────────────────────────────────────────

st.set_page_config(page_title="Cotizador Barbaratto", page_icon="📦", layout="wide")

st.markdown("""
<style>
    .block-container { max-width: 960px; padding-top: 1.5rem; }
    div[data-testid="stMetric"] { background: #f0f2f6; border-radius: 8px; padding: 12px 16px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  SESSION STATE — ROLES
# ─────────────────────────────────────────────

if "rol" not in st.session_state:
    st.session_state.rol = None

cfg = cargar_config()


# ─────────────────────────────────────────────
#  PANTALLA DE SELECCIÓN DE ROL
# ─────────────────────────────────────────────

def pantalla_login():
    st.title("📦 Cotizador Barbaratto")
    st.divider()

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.subheader("🛒 Acceso Ventas")
        st.write("Cotizá productos para clientes.")
        if st.button("**Ingresar como Ventas**", type="primary", use_container_width=True):
            st.session_state.rol = "venta"
            st.rerun()

    with col2:
        st.subheader("🔧 Acceso Manager")
        st.write("Configurá costos, márgenes y escenarios.")
        pwd = st.text_input("Contraseña", type="password", key="pwd_login")
        if st.button("**Ingresar como Manager**", use_container_width=True):
            if pwd == cfg["password_manager"]:
                st.session_state.rol = "manager"
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")


# ─────────────────────────────────────────────
#  VISTA VENTA
# ─────────────────────────────────────────────

def vista_venta():
    st.title("📦 Cotizador Barbaratto — Ventas")

    # Sidebar
    with st.sidebar:
        st.markdown("### 🛒 Modo Ventas")
        if st.button("Cerrar sesión"):
            st.session_state.rol = None
            st.rerun()

    producto = st.selectbox(
        "**Producto a cotizar**",
        ["Cajas de cartón", "Cinta de embalar", "Film stretch", "Cartón corrugado (rollos)"],
    )

    st.divider()

    # ── CAJAS ──
    if producto == "Cajas de cartón":
        st.subheader("Configuración de caja")

        tipo = st.radio(
            "Tipo de cartón",
            [f"12c — ${cfg['materiales']['12c']}/m²",
             f"17c — ${cfg['materiales']['17c']}/m²",
             f"20c — ${cfg['materiales']['20c']}/m²"],
            horizontal=True,
        )
        tipo_key = tipo[:3].strip()

        st.markdown("##### Medidas (milímetros)")
        c1, c2, c3 = st.columns(3)
        largo = c1.number_input("Largo", min_value=1, max_value=9999, value=300, step=10)
        ancho = c2.number_input("Ancho", min_value=1, max_value=9999, value=200, step=10)
        alto = c3.number_input("Alto", min_value=1, max_value=9999, value=120, step=10)

        if tipo_key == "12c":
            with st.expander("📋 Ver precios STOCK disponibles (12c)"):
                rows = [{"Medida": k, "Precio": f"${v:,} + IVA"} for k, v in cfg["stock_12c"].items()]
                st.dataframe(rows, use_container_width=True, hide_index=True)

        con_impresion = st.checkbox("Con impresión a 1 color")
        caras = 2
        if con_impresion:
            caras = st.radio("Caras impresas", [2, 4], horizontal=True)

        st.divider()
        if st.button("**Cotizar**", type="primary", use_container_width=True):
            r = cotizar_caja(cfg, tipo_key, largo, ancho, alto, con_impresion, caras)
            if r.get("error"):
                st.error("⚠️ Medidas fuera de rango. Consultar manualmente.")
            elif r["stock"]:
                st.success(f"**Precio: ${r['precio']:,.0f} + IVA** (caja STOCK {r['nombre']})")
            else:
                st.success(f"**Precio: ${r['precio']:,.2f} + IVA**")
                if r.get("cantidad_minima"):
                    st.warning(f"📦 Cantidad mínima: **{r['cantidad_minima']}**")

    # ── CINTA ──
    elif producto == "Cinta de embalar":
        st.subheader("Cinta de embalar")
        st.metric("Precio por unidad", f"${cfg['cinta']:,} + IVA")

    # ── FILM ──
    elif producto == "Film stretch":
        st.subheader("Film stretch")
        tipo_film = st.radio("Tipo", ["Transparente", "Negro"], horizontal=True)
        key = tipo_film.lower()
        st.metric(f"Precio film {key}", f"${cfg['film'][key]:,} + IVA")

    # ── CCORR ──
    elif producto == "Cartón corrugado (rollos)":
        st.subheader("Cartón corrugado en rollos")
        st.caption(f"Rollos de 120 cm — {cfg['ccorr']['peso_rollo']} kg c/u")
        cantidad = st.number_input("Cantidad de rollos", min_value=1, max_value=9999, value=1)
        total = cfg["ccorr"]["precio_kg"] * cfg["ccorr"]["peso_rollo"] * cantidad
        st.metric(f"Total ({cantidad} rollo{'s' if cantidad > 1 else ''})", f"${total:,} + IVA")
        st.caption(f"Precio por kg: ${cfg['ccorr']['precio_kg']:,}")


# ─────────────────────────────────────────────
#  VISTA MANAGER
# ─────────────────────────────────────────────

def vista_manager():
    st.title("🔧 Cotizador Barbaratto — Manager")

    with st.sidebar:
        st.markdown("### 🔧 Modo Manager")
        if st.button("Cerrar sesión"):
            st.session_state.rol = None
            st.rerun()

    tab_params, tab_sim, tab_stock = st.tabs([
        "⚙️ Parámetros de costos",
        "📊 Simulador de escenarios",
        "🏷️ Precios STOCK",
    ])

    # ═══════════════════════════════════════════
    #  TAB 1: PARÁMETROS
    # ═══════════════════════════════════════════
    with tab_params:
        st.subheader("Costos de materiales (por m²)")
        col1, col2, col3 = st.columns(3)
        mat_12c = col1.number_input("12c ($/m²)", value=float(cfg["materiales"]["12c"]), step=10.0, key="mat12")
        mat_17c = col2.number_input("17c ($/m²)", value=float(cfg["materiales"]["17c"]), step=10.0, key="mat17")
        mat_20c = col3.number_input("20c ($/m²)", value=float(cfg["materiales"]["20c"]), step=10.0, key="mat20")

        st.divider()
        st.subheader("Costos de impresión")
        ci1, ci2 = st.columns(2)
        imp_2 = ci1.number_input("2 caras ($)", value=float(cfg["impresion"]["2_caras"]), step=1.0, key="imp2")
        imp_4 = ci2.number_input("4 caras ($)", value=float(cfg["impresion"]["4_caras"]), step=1.0, key="imp4")

        st.divider()
        st.subheader("Brackets de precio — Márgenes por tipo")
        st.caption("**Tipo suma**: precio = costo + valor. **Tipo multiplicador**: precio = costo × valor.")

        for tipo_caja in ["12c", "17c", "20c"]:
            with st.expander(f"Brackets {tipo_caja}", expanded=False):
                brackets_editados = []
                for i, b in enumerate(cfg["brackets"][tipo_caja]):
                    st.markdown(f"**Rango ${b['costo_min']} – ${b['costo_max']}**")
                    bc1, bc2, bc3, bc4 = st.columns(4)
                    cmin = bc1.number_input("Costo mín", value=float(b["costo_min"]), step=10.0, key=f"bmin_{tipo_caja}_{i}")
                    cmax = bc2.number_input("Costo máx", value=float(b["costo_max"]), step=10.0, key=f"bmax_{tipo_caja}_{i}")
                    btipo = bc3.selectbox("Tipo", ["suma", "multiplicador"], index=0 if b["tipo"] == "suma" else 1, key=f"btipo_{tipo_caja}_{i}")
                    bval = bc4.number_input("Valor", value=float(b["valor"]), step=0.01, format="%.2f", key=f"bval_{tipo_caja}_{i}")
                    cant = b.get("cantidad_minima")
                    brackets_editados.append({
                        "costo_min": cmin, "costo_max": cmax,
                        "tipo": btipo, "valor": bval,
                        "cantidad_minima": cant,
                    })
                cfg["brackets"][tipo_caja] = brackets_editados

        st.divider()
        st.subheader("Productos de precio fijo")
        fp1, fp2, fp3 = st.columns(3)
        cinta_precio = fp1.number_input("Cinta ($)", value=float(cfg["cinta"]), step=10.0, key="cinta_p")
        film_t = fp2.number_input("Film transp. ($)", value=float(cfg["film"]["transparente"]), step=50.0, key="film_t")
        film_n = fp3.number_input("Film negro ($)", value=float(cfg["film"]["negro"]), step=50.0, key="film_n")

        fc1, fc2 = st.columns(2)
        ccorr_kg = fc1.number_input("Ccorr $/kg", value=float(cfg["ccorr"]["precio_kg"]), step=10.0, key="ccorr_kg")
        ccorr_peso = fc2.number_input("Ccorr kg/rollo", value=float(cfg["ccorr"]["peso_rollo"]), step=5.0, key="ccorr_peso")

        st.divider()
        if st.button("💾 **Guardar todos los parámetros**", type="primary", use_container_width=True):
            cfg["materiales"]["12c"] = mat_12c
            cfg["materiales"]["17c"] = mat_17c
            cfg["materiales"]["20c"] = mat_20c
            cfg["impresion"]["2_caras"] = imp_2
            cfg["impresion"]["4_caras"] = imp_4
            cfg["cinta"] = cinta_precio
            cfg["film"]["transparente"] = film_t
            cfg["film"]["negro"] = film_n
            cfg["ccorr"]["precio_kg"] = ccorr_kg
            cfg["ccorr"]["peso_rollo"] = int(ccorr_peso)
            guardar_config(cfg)
            st.success("✅ Parámetros guardados correctamente. Los vendedores verán los nuevos precios.")

    # ═══════════════════════════════════════════
    #  TAB 2: SIMULADOR DE ESCENARIOS
    # ═══════════════════════════════════════════
    with tab_sim:
        st.subheader("Simulador de márgenes y escenarios")
        st.caption("Ajustá los multiplicadores y compará el impacto en precio de venta vs. costo.")

        sim_tipo = st.selectbox("Tipo de cartón a simular", ["12c", "17c", "20c"], key="sim_tipo")

        st.markdown("---")
        st.markdown("##### Escenario actual vs. propuesto")
        st.caption("Modificá los valores del escenario **propuesto** para comparar.")

        # Valores actuales
        brackets_actual = cfg["brackets"][sim_tipo]
        material_actual = cfg["materiales"][sim_tipo]

        # Input escenario propuesto
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown("**Material ($/m²)**")
            mat_prop = st.number_input("Propuesto", value=float(material_actual), step=10.0, key="sim_mat")
        with sc2:
            st.markdown("**Multiplicadores propuestos por bracket**")

        propuestos = []
        for i, b in enumerate(brackets_actual):
            cc1, cc2, cc3 = st.columns([2, 1, 1])
            cc1.markdown(f"Costo ${b['costo_min']:.0f}–${b['costo_max']:.0f} ({b['tipo']})")
            val_actual = b["valor"]
            val_prop = cc2.number_input("Actual", value=float(val_actual), disabled=True, key=f"sa_{sim_tipo}_{i}")
            val_nuevo = cc3.number_input("Propuesto", value=float(val_actual), step=0.01, format="%.2f", key=f"sp_{sim_tipo}_{i}")
            propuestos.append({**b, "valor": val_nuevo})

        st.divider()

        # Generar datos para gráfico
        costos_rango = []
        for b in brackets_actual:
            step = max(1, (b["costo_max"] - b["costo_min"]) / 20)
            c = b["costo_min"] + 0.01
            while c < b["costo_max"]:
                costos_rango.append(c)
                c += step

        precios_actuales = []
        precios_propuestos = []
        margenes_actuales = []
        margenes_propuestos = []
        costos_graph = []

        for costo in costos_rango:
            # Actual
            p_act, _, _, _ = _aplicar_bracket(costo, brackets_actual)
            # Propuesto
            costo_prop = costo * (mat_prop / material_actual) if material_actual > 0 else costo
            p_prop, _, _, _ = _aplicar_bracket(costo_prop, propuestos)

            if p_act is not None and p_prop is not None:
                costos_graph.append(costo)
                precios_actuales.append(p_act)
                precios_propuestos.append(p_prop)
                margenes_actuales.append((p_act - costo) / costo * 100 if costo > 0 else 0)
                margenes_propuestos.append((p_prop - costo_prop) / costo_prop * 100 if costo_prop > 0 else 0)

        if costos_graph:
            # Gráfico 1: Precio de venta vs Costo
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=costos_graph, y=precios_actuales, name="Precio actual",
                                       line=dict(color="#2a7de1", width=2)))
            fig1.add_trace(go.Scatter(x=costos_graph, y=precios_propuestos, name="Precio propuesto",
                                       line=dict(color="#e85d2a", width=2, dash="dash")))
            fig1.add_trace(go.Scatter(x=costos_graph, y=costos_graph, name="Costo (referencia)",
                                       line=dict(color="#999", width=1, dash="dot")))
            fig1.update_layout(
                title=f"Precio de venta vs. Costo — {sim_tipo}",
                xaxis_title="Costo ($)", yaxis_title="Precio venta ($)",
                legend=dict(orientation="h", y=-0.2),
                height=420,
            )
            st.plotly_chart(fig1, use_container_width=True)

            # Gráfico 2: Margen %
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(x=costos_graph, y=margenes_actuales, name="Margen actual (%)",
                                   marker_color="#2a7de1", opacity=0.7))
            fig2.add_trace(go.Bar(x=costos_graph, y=margenes_propuestos, name="Margen propuesto (%)",
                                   marker_color="#e85d2a", opacity=0.7))
            fig2.update_layout(
                title=f"Margen de utilidad (%) — {sim_tipo}",
                xaxis_title="Costo ($)", yaxis_title="Margen (%)",
                barmode="group",
                legend=dict(orientation="h", y=-0.2),
                height=380,
            )
            st.plotly_chart(fig2, use_container_width=True)

            # Tabla resumen
            st.markdown("##### Tabla comparativa")
            df = pd.DataFrame({
                "Costo ($)": [f"${c:,.0f}" for c in costos_graph],
                "Precio actual ($)": [f"${p:,.2f}" for p in precios_actuales],
                "Precio propuesto ($)": [f"${p:,.2f}" for p in precios_propuestos],
                "Margen actual (%)": [f"{m:,.1f}%" for m in margenes_actuales],
                "Margen propuesto (%)": [f"{m:,.1f}%" for m in margenes_propuestos],
                "Diferencia ($)": [f"${(p - a):+,.2f}" for a, p in zip(precios_actuales, precios_propuestos)],
            })
            st.dataframe(df, use_container_width=True, hide_index=True)

        # Simulación puntual
        st.divider()
        st.markdown("##### Simulación puntual de una caja")
        sc1, sc2, sc3 = st.columns(3)
        sim_l = sc1.number_input("Largo (mm)", value=400, step=10, key="siml")
        sim_a = sc2.number_input("Ancho (mm)", value=300, step=10, key="sima")
        sim_h = sc3.number_input("Alto (mm)", value=200, step=10, key="simh")

        if st.button("Simular", key="btn_sim"):
            r_actual = cotizar_caja(cfg, sim_tipo, sim_l, sim_a, sim_h)
            cfg_prop = copy.deepcopy(cfg)
            cfg_prop["materiales"][sim_tipo] = mat_prop
            cfg_prop["brackets"][sim_tipo] = propuestos
            r_prop = cotizar_caja(cfg_prop, sim_tipo, sim_l, sim_a, sim_h)

            mc1, mc2 = st.columns(2)
            with mc1:
                st.markdown("**Escenario actual**")
                if r_actual.get("error"):
                    st.error("Fuera de rango")
                elif r_actual.get("stock"):
                    st.info(f"STOCK: ${r_actual['precio']:,.0f} + IVA")
                else:
                    st.metric("Precio", f"${r_actual['precio']:,.2f}",
                              delta=f"Margen: {r_actual['margen_pct']:.1f}%")
                    st.caption(f"Costo base: ${r_actual['costo_base']:,.2f}")
            with mc2:
                st.markdown("**Escenario propuesto**")
                if r_prop.get("error"):
                    st.error("Fuera de rango")
                elif r_prop.get("stock"):
                    st.info(f"STOCK: ${r_prop['precio']:,.0f} + IVA")
                else:
                    diff = r_prop["precio"] - (r_actual.get("precio", 0) or 0)
                    st.metric("Precio", f"${r_prop['precio']:,.2f}",
                              delta=f"{diff:+,.2f} vs actual")
                    st.caption(f"Costo base: ${r_prop['costo_base']:,.2f} | Margen: {r_prop['margen_pct']:.1f}%")

    # ═══════════════════════════════════════════
    #  TAB 3: PRECIOS STOCK
    # ═══════════════════════════════════════════
    with tab_stock:
        st.subheader("Precios STOCK (cajas 12c)")
        st.caption("Editá los precios de cajas con medidas estándar.")

        stock_editado = {}
        for medida, precio in cfg["stock_12c"].items():
            sc1, sc2 = st.columns([2, 1])
            sc1.markdown(f"**{medida}**")
            nuevo_precio = sc2.number_input("Precio $", value=float(precio), step=10.0, key=f"stock_{medida}", label_visibility="collapsed")
            stock_editado[medida] = nuevo_precio

        st.divider()
        if st.button("💾 **Guardar precios STOCK**", type="primary", use_container_width=True):
            cfg["stock_12c"] = stock_editado
            guardar_config(cfg)
            st.success("✅ Precios STOCK guardados.")


# ─────────────────────────────────────────────
#  ROUTER
# ─────────────────────────────────────────────

if st.session_state.rol is None:
    pantalla_login()
elif st.session_state.rol == "venta":
    vista_venta()
elif st.session_state.rol == "manager":
    vista_manager()
