"""
Fundo Las Vertientes - Sistema Fotovoltaico Agricola
Proyecto CORFO Activa Inversion: Inversion Productiva (Linea 18.4)
Resolucion Exenta N0259 - Bases Refundidas

Parametros reales:
- Inversion total tope: $50.000.000 CLP
- Cofinanciamiento CORFO: 60% (max $30.000.000)
- Aporte empresarial: 40% (min $20.000.000)
- Inversion minima proyecto: $12.000.000 CLP
- Capital de trabajo: hasta 20% del cofinanciamiento CORFO
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
from datetime import datetime, date

# -------------------------------------------------------------------------
# CONFIGURACION DE PAGINA
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="Fundo Las Vertientes - CORFO Activa Inversion",
    page_icon="\U0001F33F",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------------------------
# ESTILOS CSS
# -------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=DM+Serif+Display&display=swap');

    .stApp {
        font-family: 'DM Sans', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'DM Serif Display', serif !important;
        color: #1a3c34 !important;
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #f0f7f4 0%, #e8f5e9 100%);
        border-left: 4px solid #2e7d52;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        color: #1a3c34 !important;
    }
    .metric-card h4 {
        color: #2e7d52 !important;
        margin: 0 0 0.3rem 0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-card .value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1a3c34 !important;
    }
    .metric-card .sub {
        font-size: 0.78rem;
        color: #3d6b50 !important;
    }

    /* CORFO badge */
    .corfo-badge {
        background: linear-gradient(135deg, #1a3c34, #2e7d52);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
    }
    .corfo-badge h3 {
        color: white !important;
        margin: 0;
    }
    .corfo-badge .subtitle {
        font-size: 0.85rem;
        opacity: 0.85;
        color: white !important;
    }

    /* Alert boxes */
    .alert-ok {
        background: #e8f5e9;
        border-left: 4px solid #4caf50;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        color: #1b5e20 !important;
    }
    .alert-ok strong { color: #1b5e20 !important; }
    .alert-warn {
        background: #fff3e0;
        border-left: 4px solid #ff9800;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        color: #e65100 !important;
    }
    .alert-warn strong { color: #e65100 !important; }
    .alert-error {
        background: #ffebee;
        border-left: 4px solid #f44336;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        color: #b71c1c !important;
    }
    .alert-error strong { color: #b71c1c !important; }

    /* Table styling */
    .criteria-table {
        width: 100%;
        border-collapse: collapse;
        margin: 1rem 0;
    }
    .criteria-table th {
        background: #1a3c34;
        color: white !important;
        padding: 0.7rem;
        text-align: left;
        font-size: 0.85rem;
    }
    .criteria-table td {
        padding: 0.6rem 0.7rem;
        border-bottom: 1px solid #ccc;
        font-size: 0.85rem;
        color: #1a3c34 !important;
        background: #f5f9f7;
    }
    .criteria-table tr:nth-child(even) td {
        background: #eaf2ee;
    }

    /* Sidebar */
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a3c34 0%, #2a5c48 100%);
    }
    div[data-testid="stSidebar"] .stMarkdown h1,
    div[data-testid="stSidebar"] .stMarkdown h2,
    div[data-testid="stSidebar"] .stMarkdown h3,
    div[data-testid="stSidebar"] .stMarkdown p,
    div[data-testid="stSidebar"] .stMarkdown label {
        color: white !important;
    }

    /* ============================================= */
    /* OCULTAR BRANDING STREAMLIT (desktop + mobile) */
    /* ============================================= */
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    [data-testid="stToolbar"] {
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    [data-testid="stDecoration"] {display: none !important;}
    .block-container {padding-top: 1rem !important;}
    /* Badge, avatar, Manage app */
    div[class*="viewerBadge"] {display: none !important; height: 0 !important;}
    div[class*="profileContainer"] {display: none !important; height: 0 !important;}
    ._profileContainer_gzau3_53 {display: none !important;}
    ._container_gzau3_1 {display: none !important;}
    .viewerBadge_link__qRIco {display: none !important;}
    iframe[title="streamlit_badge"] {display: none !important;}
    [data-testid="manage-app-button"] {display: none !important;}
    .stDeployButton {display: none !important;}
    div[class*="stStatusWidget"] {display: none !important;}
    /* Barra roja inferior mobile "Alojado con Streamlit" */
    [data-testid="stBottom"] {display: none !important;}
    [data-testid="stBottomBlockContainer"] {display: none !important;}

    /* Footer personalizado */
    .custom-footer {
        text-align: center;
        padding: 1.5rem 1rem;
        margin-top: 2rem;
        border-top: 1px solid #2e7d52;
        color: #aaa !important;
        font-size: 0.8rem;
    }
    .custom-footer .dev-name {
        color: #2e7d52 !important;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .custom-footer .dev-company {
        color: #5a8a6e !important;
        font-size: 0.75rem;
        margin-top: 0.2rem;
    }
</style>
<script>
    function removeStreamlitBranding() {
        var sels = ['div[class*="viewerBadge"]','div[class*="profileContainer"]','iframe[title="streamlit_badge"]','[data-testid="manage-app-button"]','[data-testid="stBottom"]'];
        for (var i=0; i<sels.length; i++) {
            var els = document.querySelectorAll(sels[i]);
            for (var j=0; j<els.length; j++) {
                els[j].style.display='none';
                els[j].style.height='0';
                els[j].style.overflow='hidden';
            }
        }
    }
    setInterval(removeStreamlitBranding, 1500);
</script>
""", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# CONSTANTES CORFO (Bases RE-0259, Linea 18.4)
# -------------------------------------------------------------------------
CORFO_MAX_TOTAL = 50_000_000
CORFO_PCT = 0.60
CORFO_MAX_SUBSIDIO = 30_000_000
CORFO_MIN_INVERSION = 12_000_000
CAPITAL_TRABAJO_PCT_MAX = 0.20
PLAZO_MAX_MESES = 24

IRRADIACION_PEAK_HORAS = 5.2
DEGRADACION_ANUAL = 0.005
VIDA_UTIL_ANOS = 25
COSTO_MANTENCION_ANUAL_KWP = 12_000

# -------------------------------------------------------------------------
# FUNCIONES DE CALCULO
# -------------------------------------------------------------------------

def dimensionar_sistema(inversion_total, costo_kwp):
    subsidio_corfo = min(inversion_total * CORFO_PCT, CORFO_MAX_SUBSIDIO)
    aporte_empresa = inversion_total - subsidio_corfo
    capacidad_kwp = inversion_total / costo_kwp
    generacion_anual_kwh = capacidad_kwp * IRRADIACION_PEAK_HORAS * 365 * 0.80
    return {
        "inversion_total": inversion_total,
        "subsidio_corfo": subsidio_corfo,
        "aporte_empresa": aporte_empresa,
        "pct_corfo": subsidio_corfo / inversion_total * 100,
        "pct_empresa": aporte_empresa / inversion_total * 100,
        "capacidad_kwp": capacidad_kwp,
        "generacion_anual_kwh": generacion_anual_kwh,
        "generacion_mensual_kwh": generacion_anual_kwh / 12,
    }


def calcular_flujo_caja(sistema, tarifa_kwh, inflacion_tarifa, tasa_descuento,
                         consumo_mensual_kwh, precio_inyeccion_kwh, anos=25):
    flujo = []
    gen_anual = sistema["generacion_anual_kwh"]
    consumo_anual = consumo_mensual_kwh * 12
    inversion_neta = sistema["aporte_empresa"]

    for ano in range(0, anos + 1):
        if ano == 0:
            flujo.append({
                "Ano": 0, "Generacion (kWh)": 0, "Autoconsumo (kWh)": 0,
                "Inyeccion (kWh)": 0, "Ahorro Autoconsumo ($)": 0,
                "Ingreso Inyeccion ($)": 0, "Mantencion ($)": 0,
                "Flujo Neto ($)": -inversion_neta,
                "Flujo Acumulado ($)": -inversion_neta,
            })
            continue

        gen = gen_anual * (1 - DEGRADACION_ANUAL) ** ano
        autoconsumo = min(gen, consumo_anual)
        inyeccion = max(0, gen - consumo_anual)
        tarifa_ano = tarifa_kwh * (1 + inflacion_tarifa) ** ano
        precio_iny_ano = precio_inyeccion_kwh * (1 + inflacion_tarifa) ** ano
        ahorro = autoconsumo * tarifa_ano
        ingreso_iny = inyeccion * precio_iny_ano
        mantencion = sistema["capacidad_kwp"] * COSTO_MANTENCION_ANUAL_KWP * (1 + 0.03) ** ano
        flujo_neto = ahorro + ingreso_iny - mantencion
        acumulado = flujo[-1]["Flujo Acumulado ($)"] + flujo_neto

        flujo.append({
            "Ano": ano, "Generacion (kWh)": round(gen),
            "Autoconsumo (kWh)": round(autoconsumo),
            "Inyeccion (kWh)": round(inyeccion),
            "Ahorro Autoconsumo ($)": round(ahorro),
            "Ingreso Inyeccion ($)": round(ingreso_iny),
            "Mantencion ($)": round(mantencion),
            "Flujo Neto ($)": round(flujo_neto),
            "Flujo Acumulado ($)": round(acumulado),
        })

    return pd.DataFrame(flujo)


def calcular_tir(df_flujo):
    flujos = df_flujo["Flujo Neto ($)"].values
    try:
        tir = 0.10
        for _ in range(1000):
            npv = sum(f / (1 + tir) ** t for t, f in enumerate(flujos))
            dnpv = sum(-t * f / (1 + tir) ** (t + 1) for t, f in enumerate(flujos))
            if abs(dnpv) < 1e-12:
                break
            tir_new = tir - npv / dnpv
            if abs(tir_new - tir) < 1e-8:
                tir = tir_new
                break
            tir = tir_new
        return tir
    except Exception:
        return None


def calcular_van(df_flujo, tasa):
    flujos = df_flujo["Flujo Neto ($)"].values
    return sum(f / (1 + tasa) ** t for t, f in enumerate(flujos))


def calcular_payback(df_flujo):
    for _, row in df_flujo.iterrows():
        if row["Ano"] > 0 and row["Flujo Acumulado ($)"] >= 0:
            return int(row["Ano"])
    return None


def verificar_admisibilidad(sistema):
    checks = []
    inv = sistema["inversion_total"]
    checks.append(("Inversion >= $12.000.000", inv >= CORFO_MIN_INVERSION,
                    f"${inv:,.0f}".replace(",", ".")))
    checks.append(("Subsidio CORFO <= $30.000.000", sistema["subsidio_corfo"] <= CORFO_MAX_SUBSIDIO,
                    f"${sistema['subsidio_corfo']:,.0f}".replace(",", ".")))
    checks.append(("% CORFO <= 60%", sistema["pct_corfo"] <= 60.01,
                    f"{sistema['pct_corfo']:.1f}%"))
    checks.append(("Inversion total <= $50.000.000", inv <= CORFO_MAX_TOTAL,
                    f"${inv:,.0f}".replace(",", ".")))
    return checks


# -------------------------------------------------------------------------
# SIDEBAR - PARAMETROS DEL PROYECTO
# -------------------------------------------------------------------------
with st.sidebar:
    st.markdown("# \U0001F33F Fundo Las Vertientes")
    st.markdown("### Parametros del Proyecto")
    st.markdown("---")

    st.markdown("#### \U0001F4B0 Inversion")
    inversion_total = st.slider(
        "Inversion total del proyecto ($CLP)",
        min_value=12_000_000, max_value=50_000_000, value=48_000_000,
        step=1_000_000, format="$%d",
    )
    costo_kwp = st.slider(
        "Costo instalado por kWp ($CLP)",
        min_value=800_000, max_value=1_800_000, value=1_200_000,
        step=50_000, format="$%d",
        help="Incluye paneles, inversores, estructura, instalacion y permisos SEC",
    )

    st.markdown("#### \u26A1 Consumo y Tarifas")
    consumo_mensual = st.slider("Consumo mensual del fundo (kWh)",
        min_value=500, max_value=8_000, value=2_800, step=100)
    tarifa_kwh = st.slider("Tarifa electrica ($/kWh)",
        min_value=80, max_value=250, value=155, step=5,
        help="Tarifa BT promedio zona central agricola")
    precio_inyeccion = st.slider("Precio inyeccion Net Billing ($/kWh)",
        min_value=40, max_value=150, value=85, step=5,
        help="Precio regulado de inyeccion a la red")

    st.markdown("#### \U0001F4C8 Proyecciones")
    inflacion_tarifa = st.slider("Inflacion tarifa electrica anual (%)",
        min_value=0.0, max_value=8.0, value=3.5, step=0.5) / 100
    tasa_descuento = st.slider("Tasa de descuento (%)",
        min_value=4.0, max_value=15.0, value=8.0, step=0.5) / 100

    st.markdown("---")
    st.markdown("""
    <div style='text-align:center; opacity:0.7; font-size:0.75rem; color:#ccc;'>
    Bases: RE N0259/2020<br>
    Linea 18.4 Inversion Productiva<br>
    Gerencia Redes y Competitividad
    </div>
    """, unsafe_allow_html=True)


# -------------------------------------------------------------------------
# CALCULOS PRINCIPALES
# -------------------------------------------------------------------------
sistema = dimensionar_sistema(inversion_total, costo_kwp)
df_flujo = calcular_flujo_caja(sistema, tarifa_kwh, inflacion_tarifa, tasa_descuento, consumo_mensual, precio_inyeccion)
tir = calcular_tir(df_flujo)
van = calcular_van(df_flujo, tasa_descuento)
payback = calcular_payback(df_flujo)
checks = verificar_admisibilidad(sistema)

# -------------------------------------------------------------------------
# HEADER
# -------------------------------------------------------------------------
st.markdown("""
<div class='corfo-badge'>
    <h3>CORFO ACTIVA INVERSION - INVERSION PRODUCTIVA</h3>
    <div class='subtitle'>Resolucion Exenta N0259 - Linea 18.4 - Fundo Las Vertientes</div>
</div>
""", unsafe_allow_html=True)

st.markdown("## Sistema Fotovoltaico para Produccion Agricola")
st.markdown("Proyecto de inversion productiva en energia solar para operaciones agricolas, "
    "dimensionado conforme a las Bases refundidas del instrumento Activa Inversion de CORFO.")

# -------------------------------------------------------------------------
# TAB LAYOUT
# -------------------------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Resumen Ejecutivo", "Sistema Fotovoltaico", "Flujo de Caja",
    "Admisibilidad CORFO", "Criterios de Evaluacion",
])

# -------------------------------------------------------------------------
# TAB 1: RESUMEN EJECUTIVO
# -------------------------------------------------------------------------
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""<div class='metric-card'><h4>Inversion Total</h4>
            <div class='value'>${inversion_total/1e6:.1f}M</div>
            <div class='sub'>Tope: $50M CLP</div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div class='metric-card'><h4>Subsidio CORFO (60%)</h4>
            <div class='value'>${sistema["subsidio_corfo"]/1e6:.1f}M</div>
            <div class='sub'>Maximo: $30M CLP</div></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""<div class='metric-card'><h4>Aporte Empresarial (40%)</h4>
            <div class='value'>${sistema["aporte_empresa"]/1e6:.1f}M</div>
            <div class='sub'>{sistema["pct_empresa"]:.0f}% del total</div></div>""", unsafe_allow_html=True)
    with col4:
        tir_display = f"{tir*100:.1f}%" if tir else "N/A"
        st.markdown(f"""<div class='metric-card'><h4>TIR del Proyecto</h4>
            <div class='value'>{tir_display}</div>
            <div class='sub'>Tasa desc.: {tasa_descuento*100:.0f}%</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("### Indicadores Financieros")
        van_display = f"${van:,.0f}".replace(",", ".") if van else "N/A"
        payback_display = f"{payback} anos" if payback else "> 25 anos"
        ind_data = {
            "Indicador": ["Valor Actual Neto (VAN)", "Tasa Interna de Retorno (TIR)",
                "Payback (recuperacion inversion empresario)", "Generacion anual",
                "Capacidad instalada", "Ratio beneficio/costo"],
            "Valor": [van_display, tir_display, payback_display,
                f"{sistema['generacion_anual_kwh']:,.0f} kWh".replace(",", "."),
                f"{sistema['capacidad_kwp']:.1f} kWp",
                f"{(van + sistema['aporte_empresa']) / sistema['aporte_empresa']:.2f}x" if van and van > 0 else "< 1x"],
        }
        st.table(pd.DataFrame(ind_data).set_index("Indicador"))

    with col_b:
        st.markdown("### Estructura de Financiamiento")
        chart_data = pd.DataFrame({"Fuente": ["CORFO (60%)", "Empresario (40%)"],
            "Monto": [sistema["subsidio_corfo"], sistema["aporte_empresa"]]})
        st.bar_chart(chart_data.set_index("Fuente"), horizontal=True)
        kdt_max = sistema["subsidio_corfo"] * CAPITAL_TRABAJO_PCT_MAX
        st.markdown(f"""<div class='alert-ok'>
            Capital de trabajo admisible: hasta ${kdt_max:,.0f} CLP (20% del subsidio CORFO) - Ref. Bases Art. 18.4.e
            </div>""".replace(",", "."), unsafe_allow_html=True)


# -------------------------------------------------------------------------
# TAB 2: SISTEMA FOTOVOLTAICO
# -------------------------------------------------------------------------
with tab2:
    st.markdown("### Dimensionamiento del Sistema")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Capacidad Instalada", f"{sistema['capacidad_kwp']:.1f} kWp")
        n_paneles_550 = int(np.ceil(sistema["capacidad_kwp"] * 1000 / 550))
        st.metric("Paneles (550W)", f"{n_paneles_550} unidades")
    with col2:
        st.metric("Generacion Anual", f"{sistema['generacion_anual_kwh']:,.0f} kWh")
        st.metric("Generacion Mensual", f"{sistema['generacion_mensual_kwh']:,.0f} kWh")
    with col3:
        autoconsumo_pct = min(consumo_mensual * 12 / sistema["generacion_anual_kwh"] * 100, 100)
        st.metric("% Autoconsumo", f"{autoconsumo_pct:.0f}%")
        st.metric("Excedente Inyeccion", f"{max(0, 100-autoconsumo_pct):.0f}%")

    st.markdown("---")
    st.markdown("### Generacion Mensual Estimada (Ano 1)")
    hsp_mensual = [6.8, 6.2, 5.4, 4.2, 3.2, 2.6, 2.8, 3.5, 4.5, 5.5, 6.3, 6.9]
    meses = ["Ene","Feb","Mar","Abr","May","Jun","Jul","Ago","Sep","Oct","Nov","Dic"]
    dias_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gen_mensual = [round(sistema["capacidad_kwp"] * hsp_mensual[i] * dias_mes[i] * 0.80) for i in range(12)]
    df_mensual = pd.DataFrame({"Mes": meses, "Generacion (kWh)": gen_mensual, "Consumo (kWh)": [consumo_mensual]*12}).set_index("Mes")
    st.bar_chart(df_mensual)

    st.markdown("### Especificaciones Tecnicas Sugeridas")
    specs = pd.DataFrame({
        "Componente": ["Paneles solares","Inversor(es)","Estructura montaje","Protecciones y tablero","Medidor bidireccional","Cableado y conectores","Ingenieria y permisos SEC"],
        "Especificacion": [
            f"{n_paneles_550}x modulos monocristalinos 550W Tier-1",
            f"Inversor(es) string {sistema['capacidad_kwp']:.0f}kW, MPPT multiple",
            "Estructura aluminio para techumbre o suelo agricola",
            "Protecciones DC/AC, SPD, interruptor de corte",
            "Medidor bidireccional homologado SEC/distribuidora",
            "Cable solar 4/6mm2, MC4, canalizacion",
            "Declaracion TE1/TE4, inscripcion SEC, Net Billing"],
        "% Presupuesto": ["45%","20%","10%","5%","3%","5%","12%"],
    })
    st.table(specs.set_index("Componente"))


# -------------------------------------------------------------------------
# TAB 3: FLUJO DE CAJA
# -------------------------------------------------------------------------
with tab3:
    st.markdown("### Flujo de Caja Proyectado a 25 Anos")
    st.markdown(f"*Inversion neta empresario: ${sistema['aporte_empresa']:,.0f} CLP - Tasa descuento: {tasa_descuento*100:.0f}% - Inflacion tarifa: {inflacion_tarifa*100:.1f}%*".replace(",", "."))

    st.markdown("#### Flujo Acumulado ($CLP)")
    chart_flujo = df_flujo[df_flujo["Ano"] > 0][["Ano", "Flujo Acumulado ($)"]].set_index("Ano")
    st.line_chart(chart_flujo)

    if payback:
        st.markdown(f"""<div class='alert-ok'>
            Payback en ano {payback}: la inversion del empresario (${sistema['aporte_empresa']:,.0f} CLP)
            se recupera en {payback} anos. Vida util restante: {25 - payback} anos de beneficio neto.
            </div>""".replace(",", "."), unsafe_allow_html=True)
    else:
        st.markdown("""<div class='alert-warn'>El payback excede la vida util. Considere ajustar parametros.</div>""", unsafe_allow_html=True)

    st.markdown("#### Detalle Anual")
    df_display = df_flujo.copy()
    for c in [c for c in df_display.columns if "($)" in c]:
        df_display[c] = df_display[c].apply(lambda x: f"${x:,.0f}".replace(",", "."))
    for c in [c for c in df_display.columns if "(kWh)" in c]:
        df_display[c] = df_display[c].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    st.dataframe(df_display, use_container_width=True, height=400)

    st.markdown("#### Composicion de Ingresos Anuales")
    df_ingresos = df_flujo[df_flujo["Ano"] > 0][["Ano", "Ahorro Autoconsumo ($)", "Ingreso Inyeccion ($)"]].set_index("Ano")
    st.area_chart(df_ingresos)


# -------------------------------------------------------------------------
# TAB 4: ADMISIBILIDAD CORFO
# -------------------------------------------------------------------------
with tab4:
    st.markdown("### Verificacion de Admisibilidad - Bases Art. 18.4.f")
    st.markdown("Requisitos de admisibilidad especificos del postulante y del proyecto, "
        "conforme al numeral 18.4 letra f) de las Bases refundidas RE N0259.")

    all_ok = True
    for criterio, cumple, valor in checks:
        icon = "OK" if cumple else "NO"
        css_class = "alert-ok" if cumple else "alert-error"
        st.markdown(f"<div class='{css_class}'><strong>{criterio}</strong>: {valor}</div>", unsafe_allow_html=True)
        if not cumple:
            all_ok = False

    st.markdown("---")
    st.markdown("### Requisitos del Postulante (Art. 18.4.c y 18.4.f.a)")
    estado_inv = "OK" if inversion_total >= CORFO_MIN_INVERSION else "NO"
    st.markdown(f"""
    <table class='criteria-table'>
        <tr><th>Requisito</th><th>Referencia Bases</th><th>Estado</th></tr>
        <tr><td>Contribuyente 1a Categoria, art. 20 DL 824/1974</td><td>Art. 18.4.c num. 1</td><td>Verificar en SII</td></tr>
        <tr><td>Ventas netas anuales >= 5.000 UF (si Gerente autoriza)</td><td>Art. 18.4.c num. 2</td><td>Revisar F29</td></tr>
        <tr><td>Proyecto inversion >= $12.000.000 CLP</td><td>Art. 18.4.f.b num. 1</td><td>{estado_inv} Cumple</td></tr>
        <tr><td>Participacion Estado &lt; 40% en capital/patrimonio</td><td>Art. 4</td><td>Empresa privada</td></tr>
        <tr><td>No empresa publica ni sociedad estatal</td><td>Art. 4</td><td>Cumple</td></tr>
        <tr><td>Inscripcion Registro Personas Juridicas CORFO</td><td>Art. 15.2</td><td>Verificar/inscribir</td></tr>
        <tr><td>Cotizaciones sociales y seguros al dia</td><td>Art. 17.2 letra B</td><td>Verificar</td></tr>
        <tr><td>Impuestos al dia (art. 20 nums. 3, 4 y 5)</td><td>Art. 17.2 letra B</td><td>Verificar F29</td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Documentos Requeridos para Formalizacion (Art. 15.1)")
    for d in ["Cedula de identidad del representante legal (ambos lados)",
              "Escritura publica o instrumento de constitucion",
              "Extracto inscripcion en Registro de Comercio (3 meses max)",
              "Extracto publicacion constitucion en Diario Oficial",
              "Escritura de personeria del representante legal",
              "Formulario 29 SII (ultimos 12 meses)",
              "Libro Auxiliar de Compras y Ventas (periodo anterior)",
              "Balance y/o Estado de Resultados"]:
        st.markdown(f"- {d}")

    if not all_ok:
        st.markdown("<div class='alert-error'><strong>PROYECTO NO ADMISIBLE</strong> - Ajuste los parametros para cumplir con los requisitos de las Bases.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='alert-ok'><strong>PROYECTO ADMISIBLE</strong> - Todos los criterios cuantitativos de admisibilidad se cumplen. Verificar requisitos documentales pendientes.</div>", unsafe_allow_html=True)


# -------------------------------------------------------------------------
# TAB 5: CRITERIOS DE EVALUACION
# -------------------------------------------------------------------------
with tab5:
    st.markdown("### Criterios de Evaluacion - Ponderaciones (Art. 13 y 18.4.g)")
    st.markdown("La evaluacion se realiza con puntaje de 1 a 5. No se recomiendan proyectos con nota final < 3 o con algun criterio < 2,50.")

    st.markdown("#### Criterios Comunes (60%)")
    st.markdown("""
    <table class='criteria-table'>
        <tr><th>Criterio</th><th>Pond.</th><th>Elementos evaluados</th></tr>
        <tr><td><strong>Impacto economico del proyecto</strong></td><td>25%</td><td>Diversificacion matriz productiva, competitividad industria, cierre brechas, sustentabilidad medioambiental</td></tr>
        <tr><td><strong>Calidad formulacion y coherencia</strong></td><td>10%</td><td>Coherencia beneficiarios-objetivo, actividades-plazos-resultados</td></tr>
        <tr><td><strong>Propuesta economica</strong></td><td>15%</td><td>Coherencia presupuesto vs actividades y resultados</td></tr>
        <tr><td><strong>Justificacion territorial</strong></td><td>10%</td><td>Pertinencia respecto a lineamientos de desarrollo regional y de CORFO</td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("#### Criterios Especificos Linea 18.4 (40%)")
    st.markdown("""
    <table class='criteria-table'>
        <tr><th>Criterio</th><th>Pond.</th><th>Elementos evaluados</th></tr>
        <tr><td><strong>Fortaleza del proyecto de inversion</strong></td><td>20%</td><td>Plan de negocios, rentabilidad, acceso a financiamiento, generacion empleo</td></tr>
        <tr><td><strong>Fortaleza de la empresa</strong></td><td>20%</td><td>Experiencia en el sector, coherencia estrategia vs proyecto de inversion</td></tr>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### Argumentos para la Postulacion")
    ahorro_anual_1 = df_flujo[df_flujo["Ano"] == 1]["Ahorro Autoconsumo ($)"].values[0]
    ingreso_anual_1 = df_flujo[df_flujo["Ano"] == 1]["Ingreso Inyeccion ($)"].values[0]

    st.markdown(f"#### Impacto Economico (25%)")
    st.markdown(f"- Ahorro energetico ano 1: ${ahorro_anual_1:,.0f} CLP\n- Ingreso por inyeccion ano 1: ${ingreso_anual_1:,.0f} CLP (Net Billing)\n- Reduccion huella de carbono: ~{sistema['generacion_anual_kwh'] * 0.0004:.1f} tonCO2/ano\n- Aumento competitividad: reduccion de costos fijos en produccion agricola".replace(",", "."))

    st.markdown(f"#### Calidad y Coherencia (10%)")
    st.markdown(f"- Sistema dimensionado segun consumo real del fundo ({consumo_mensual} kWh/mes)\n- Presupuesto detallado con cotizaciones de proveedores Tier-1\n- Plazo ejecucion: 6-8 meses (dentro del maximo de 24 meses)\n- Resultados medibles: kWh generados, ahorro en $, reduccion CO2")

    st.markdown(f"#### Propuesta Economica (15%)")
    st.markdown(f"- VAN positivo: {van_display} a tasa {tasa_descuento*100:.0f}%\n- TIR: {tir_display} (supera costo de oportunidad)\n- Payback: {payback_display}\n- Presupuesto coherente con precios de mercado ({costo_kwp:,}/kWp instalado)".replace(",", "."))

    st.markdown(f"#### Justificacion Territorial (10%)")
    st.markdown("- Zona rural agricola con alta irradiacion solar\n- Contribuye a diversificacion energetica regional\n- Fortalece competitividad de productores agricolas locales\n- Alineado con estrategia regional de desarrollo sustentable")

    st.markdown(f"#### Fortaleza del Proyecto (20%)")
    st.markdown(f"- Rentabilidad demostrada con TIR {tir_display} y VAN positivo\n- Tecnologia madura y probada (solar fotovoltaica)\n- Sin requerimiento de financiamiento externo adicional\n- Generacion de empleo en instalacion y mantencion")

    st.markdown(f"#### Fortaleza de la Empresa (20%)")
    st.markdown("- Empresa agricola con trayectoria productiva demostrable\n- Experiencia en gestion de proyectos de inversion\n- Capacidad financiera para aportar el 40% requerido\n- Coherencia estrategica: energia solar reduce costos operativos permanentemente")


# -------------------------------------------------------------------------
# FOOTER
# -------------------------------------------------------------------------
st.markdown(
    f"""<div class='custom-footer'>
        Fundo Las Vertientes - Proyecto CORFO Activa Inversion -
        Bases RE N0259 Linea 18.4 Inversion Productiva -
        Generado: {datetime.now().strftime('%d/%m/%Y')}
        <div class='dev-name'>Desarrollado por Jose A. Eyzaguirre R.</div>
        <div class='dev-company'>Fundador de Makey E.I.R.L.</div>
    </div>""",
    unsafe_allow_html=True,
)
