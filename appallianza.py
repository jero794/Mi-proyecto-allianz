
import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from etfs_data import ETFs_Data
import numpy as np
from io import BytesIO



# Configuración de la página y estilo
st.set_page_config(page_title="Simulador Financiero de ETFs - Allianz Patrimonial", layout="centered")
st.markdown(
    """
    <style>
    .stApp {background-color: #F8F9FA;}
    h1, h2, h3, h4 {color: #004B87;}
    .css-1lcbmhc {padding-top: 1.5rem;}
    .metric {display: inline-block; margin: 0 2em;}
    </style>
    """, unsafe_allow_html=True
)

# Título de la aplicación
st.title("Análisis de ETFs")

#### Selector de Datos ####
etfs_seleccionados = st.multiselect(
    "Selecciona uno o más ETFs para ver los detalles:",
    options=[etf['nombre'] for etf in ETFs_Data],
    default=[]
)

if etfs_seleccionados:
    st.write("### Detalles de los ETFs Seleccionados:")
    for etf_name in etfs_seleccionados:
        etf_info = next((etf for etf in ETFs_Data if etf['nombre'] == etf_name), None)
        if etf_info:
            st.write(f"**Nombre**: {etf_info['nombre']}")
            st.write(f"**Descripción**: {etf_info['descripcion']}")
            st.write(f"**Símbolo**: {etf_info['simbolo']}")
            st.markdown("---")
else:
    st.write("Por favor, selecciona al menos un ETF para ver los detalles.")

# Función para obtener datos financieros de un ETF de Yahoo Finance
def obtener_datos_etf(ticker, periodo):
    etf = yf.Ticker(ticker)
    datos = etf.history(period=periodo)
    return datos

# Selección de ETF y periodo de análisis
etf_seleccionado = st.selectbox("Selecciona el ETF", ("SPY", "QQQ", "DIA", "XLF", "VWO", "XLV", "ITB", "SLV", "EWU", "EWT", "EWY", "EZU", "EWC", "EWJ", "EWG", "EWA", "AGG"))   
periodo_seleccionado = st.selectbox("Selecciona el periodo", ("1mo", "3mo", "6mo", "1y", "3y", "5y", "10y"))

datos_etf = obtener_datos_etf(etf_seleccionado, periodo_seleccionado)

# Organizar gráficos en pestañas
tab1, tab2, tab3 = st.tabs(["Rendimiento y Riesgo", "Ratios Financieros", "Análisis de Precios"])

# Pestaña 1: Rendimiento y Riesgo
# Resto de tu código aquí...

# Después de la sección de rendimiento y riesgo en la pestaña 1:
with tab1:
    st.write(f"### Rendimiento y Riesgo para {etf_seleccionado}")
    if not datos_etf.empty:
        # Cálculo de rendimiento y riesgo
        def calcular_rendimiento_riesgo(datos):
            rendimiento = datos['Close'].pct_change().mean() * 252
            riesgo = datos['Close'].pct_change().std() * (252 ** 0.5)
            return rendimiento, riesgo

        rendimiento, riesgo = calcular_rendimiento_riesgo(datos_etf)
        
        # Panel de métricas clave
        col1, col2 = st.columns(2)
        col1.metric(label="Rendimiento Anualizado", value=f"{rendimiento:.2%}")
        col2.metric(label="Riesgo (Desviación Estándar)", value=f"{riesgo:.2%}")

        # Ingreso del monto a invertir (con formato de moneda)
        monto_inversion_texto = st.text_input("Ingresa el monto que deseas invertir (en USD):", value="0")

        # Remover el símbolo de dólar y las comas, y convertir a número
        try:
            monto_inversion = float(monto_inversion_texto.replace(",", "").replace("$", ""))
        except ValueError:
            monto_inversion = 0.0  # Valor predeterminado si la conversión falla

        # Formatear el monto de entrada con el signo de dólar y comas
        monto_inversion_formateado = f"${monto_inversion:,.2f}"
        st.text_input("Monto ingresado:", value=monto_inversion_formateado, disabled=True)

        # Cálculo del monto final considerando el rendimiento
        if monto_inversion > 0:
            monto_final = monto_inversion * (1 + rendimiento)  # Monto final tras el rendimiento
            st.write(f"### Monto estimado al finalizar el periodo: ${monto_final:,.2f}")



        # Gráfico de rendimiento
        st.write("### Gráfico de Precio de Cierre")
        fig, ax = plt.subplots()
        sns.lineplot(data=datos_etf, x=datos_etf.index, y="Close", ax=ax, color="blue")
        ax.set_title(f"Precio de Cierre de {etf_seleccionado}")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Precio de Cierre (USD)")
        st.pyplot(fig)
    else:
        st.write("No se encontraron datos para el ETF seleccionado en el periodo especificado.")


# Pestaña 2: Ratios Financieros
with tab2:
    st.write("### Ratios Financieros")

    if not datos_etf.empty:
        # Ratio de Sharpe
        def calcular_sharpe_ratio(datos, tasa_libre_riesgo=0.02):
            retorno_exceso = datos['Close'].pct_change() - (tasa_libre_riesgo / 252)
            ratio_sharpe = (retorno_exceso.mean() * 252) / (retorno_exceso.std() * np.sqrt(252))
            return ratio_sharpe

        # Ratio de Sortino
        def calcular_sortino_ratio(datos, tasa_libre_riesgo=0.02):
            retorno_exceso = datos['Close'].pct_change() - (tasa_libre_riesgo / 252)
            downside_deviation = retorno_exceso[retorno_exceso < 0].std() * np.sqrt(252)
            ratio_sortino = (retorno_exceso.mean() * 252) / downside_deviation
            return ratio_sortino

        # VaR (Valor en Riesgo) al 95%
        def calcular_var(datos, nivel_confianza=0.05):
            var_95 = np.percentile(datos['Close'].pct_change().dropna(), nivel_confianza * 100)
            return var_95

        sharpe_ratio = calcular_sharpe_ratio(datos_etf)
        sortino_ratio = calcular_sortino_ratio(datos_etf)
        var_95 = calcular_var(datos_etf)

        st.write(f"**Ratio de Sharpe:** {sharpe_ratio:.2f}")
        st.write(f"**Ratio de Sortino:** {sortino_ratio:.2f}")
        st.write(f"**Valor en Riesgo (VaR) al 95%:** {var_95:.2%}")
    else:
        st.write("No se encontraron datos para el ETF seleccionado en el periodo especificado.")

# Pestaña 3: Análisis de Precios
with tab3:
    st.write("### Análisis de Precios")
    st.write(f"Visualización de precios históricos de {etf_seleccionado} y otros análisis.")
    
    fig, ax = plt.subplots()
    sns.histplot(datos_etf['Close'].pct_change().dropna(), kde=True, color="green")
    ax.set_title("Distribución de Cambios Diarios de Precio")
    ax.set_xlabel("Cambio Diario (%)")
    ax.set_ylabel("Frecuencia")
    st.pyplot(fig)

# Botón de descarga de datos
if not datos_etf.empty:
    buffer = BytesIO()
    datos_etf.to_csv(buffer)
    buffer.seek(0)
    
    st.download_button(
        label="Descargar datos del ETF en CSV",
        data=buffer,
        file_name=f"{etf_seleccionado}_datos.csv",
        mime="text/csv"
    )

# Sección de comparación con un botón desplegable
with st.expander("Click para comparar el rendimiento y riesgo de dos ETFs", expanded=False):
    # Selección de dos ETFs para comparar
    etf_1 = st.selectbox("Selecciona el primer ETF", ("SPY", "QQQ", "DIA", "XLF", "VWO", "XLV", "ITB", "SLV", "EWU", "EWT", "EWY", "EZU", "EWC", "EWJ", "EWG", "EWA", "AGG"), key="etf_1_comparacion")
    etf_2 = st.selectbox("Selecciona el segundo ETF", ("SPY", "QQQ", "DIA", "XLF", "VWO", "XLV", "ITB", "SLV", "EWU", "EWT", "EWY", "EZU", "EWC", "EWJ", "EWG", "EWA", "AGG"), key="etf_2_comparacion")

    # Período de análisis para ambos ETFs
    periodo_comparacion = st.selectbox("Selecciona el periodo para la comparación", ("1mo", "3mo", "6mo", "1y", "3y", "5y", "10y"), key="periodo_comparacion")

    # Obtener datos y calcular métricas para ambos ETFs
    datos_etf_1 = obtener_datos_etf(etf_1, periodo_comparacion)
    datos_etf_2 = obtener_datos_etf(etf_2, periodo_comparacion)

    if not datos_etf_1.empty and not datos_etf_2.empty:
        # Calcular rendimiento, riesgo y Sharpe ratio para el primer ETF
        rendimiento_1, riesgo_1 = calcular_rendimiento_riesgo(datos_etf_1)
        sharpe_ratio_1 = calcular_sharpe_ratio(datos_etf_1)

        # Calcular rendimiento, riesgo y Sharpe ratio para el segundo ETF
        rendimiento_2, riesgo_2 = calcular_rendimiento_riesgo(datos_etf_2)
        sharpe_ratio_2 = calcular_sharpe_ratio(datos_etf_2)

        # Mostrar las métricas en dos columnas
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"### {etf_1}")
            st.metric("Rendimiento Anualizado", f"{rendimiento_1:.2%}")
            st.metric("Riesgo (Desviación Estándar)", f"{riesgo_1:.2%}")
            st.metric("Ratio de Sharpe", f"{sharpe_ratio_1:.2f}")

        with col2:
            st.write(f"### {etf_2}")
            st.metric("Rendimiento Anualizado", f"{rendimiento_2:.2%}")
            st.metric("Riesgo (Desviación Estándar)", f"{riesgo_2:.2%}")
            st.metric("Ratio de Sharpe", f"{sharpe_ratio_2:.2f}")
    else:
        st.write("No se encontraron datos para uno o ambos ETFs en el periodo especificado.")

# Sección: 10 ETFs con mejor rendimiento
st.write("## 10 ETFs con mejor rendimiento conforme al periodo seleccionado")

# Selector de periodo
periodo_ranking = st.selectbox(
    "Selecciona el periodo para el ranking:",
    options=["1mo", "3mo", "6mo", "1y", "3y", "5y", "10y"]
)

# Función para calcular rendimientos y riesgos para todos los ETFs
def calcular_rendimientos_y_riesgos(etfs_data, periodo):
    rendimiento_riesgo = []
    for etf in etfs_data:
        ticker = etf["simbolo"]
        datos = obtener_datos_etf(ticker, periodo)
        if not datos.empty:
            rendimiento = datos['Close'].pct_change().mean() * 252  # Rendimiento anualizado
            riesgo = datos['Close'].pct_change().std() * (252 ** 0.5)  # Riesgo (desviación estándar anualizada)
            rendimiento_riesgo.append({
                "nombre": etf["nombre"],
                "rendimiento": rendimiento,
                "riesgo": riesgo
            })
    return rendimiento_riesgo

# Obtener y procesar datos para el ranking
ranking = calcular_rendimientos_y_riesgos(ETFs_Data, periodo_ranking)

# Ordenar por rendimiento en orden descendente y seleccionar los 10 mejores
ranking_top_10 = sorted(ranking, key=lambda x: x["rendimiento"], reverse=True)[:10]

# Mostrar resultados en una tabla
if ranking_top_10:
    st.write("### Ranking de los 10 mejores ETFs")
    for idx, etf in enumerate(ranking_top_10, start=1):
        st.write(f"{idx}. **{etf['nombre']}** - Rendimiento: {etf['rendimiento']:.2%} | Riesgo: {etf['riesgo']:.2%}")
else:
    st.write("No se encontraron datos para los ETFs en el periodo seleccionado.")




# Crear el DataFrame de ETFs
df_etfs = pd.DataFrame(etf_data)

# Título
st.title("¡TIA MYRIAM VAMOS A INVERTIR!")

# Mostrar los ETFs disponibles
st.subheader("Los ETFs disponibles:")
st.dataframe(df_etfs)

# Ingresar la cantidad a invertir
cantidad_total = st.number_input("¿Cuánto dinero deseas invertir? (en dólares):", min_value=1.0, step=1.0)

# Seleccionar hasta 4 ETFs
etfs_seleccionados = st.multiselect(
    "Selecciona hasta 4 ETFs para diversificar tu portafolio:",
    options=df_etfs["ETF"].values,
    max_selections=4
)

# Asignar los porcentajes para cada ETF
porcentajes = {}
if etfs_seleccionados:
    st.subheader("Asigna un porcentaje de inversión a cada ETF seleccionado.")
    total_percentage = 0
    for etf in etfs_seleccionados:
        porcentaje = st.slider(f"Porcentaje para {etf}", 0, 100, 100 - total_percentage, step=1)
        porcentajes[etf] = porcentaje / 100
        total_percentage += porcentaje

# Calcular el rendimiento y el riesgo del portafolio
if len(etfs_seleccionados) > 0:
    df_seleccionados = df_etfs[df_etfs["ETF"].isin(etfs_seleccionados)].copy()
    df_seleccionados["Asignación"] = df_seleccionados["ETF"].map(porcentajes).fillna(0)

    rendimiento_portafolio = (df_seleccionados["Rendimiento"] * df_seleccionados["Asignación"]).sum()
    riesgo_portafolio = np.sqrt((df_seleccionados["Riesgo"] ** 2 * df_seleccionados["Asignación"]).sum())

    # Mostrar los resultados de la diversificación
    st.subheader("Resultados de la diversificación:")
    st.write(f"Rendimiento del portafolio: {rendimiento_portafolio:.2%}")
    st.write(f"Riesgo del portafolio: {riesgo_portafolio:.2%}")
else:
    st.warning("Por favor, selecciona al menos un ETF y asigna un porcentaje.")