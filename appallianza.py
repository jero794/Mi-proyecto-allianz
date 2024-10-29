import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from etfs_data import ETFs_Data

# Configuración de la página y estilo
st.set_page_config(page_title="Simulador Financiero de ETFs - Allianz Patrimonial", layout="centered")
st.markdown(
    """
    <style>
    .stApp {background-color: #F8F9FA;}
    h1, h2, h3, h4 {color: #004B87;}
    .css-1lcbmhc {padding-top: 1.5rem;}
    </style>
    """, unsafe_allow_html=True
)

# Título de la aplicación
st.title("Análisis de ETFs")

#### Selector de Datos ####
# Crear un multiselector usando st.multiselect
etfs_seleccionados = st.multiselect(
    "Selecciona uno o más ETFs para ver los detalles:",
    options=[etf['nombre'] for etf in ETFs_Data],  # Opciones basadas en los nombres de los ETFs
    default=[]  # Por defecto no seleccionamos ninguno
)

# Verificar si hay algún ETF seleccionado
if etfs_seleccionados:
    st.write("### Detalles de los ETFs Seleccionados:")
    for etf_name in etfs_seleccionados:
        # Buscar en la lista ETFs_Data el diccionario que tenga ese nombre
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

# Cálculo de rendimiento y riesgo
def calcular_rendimiento_riesgo(datos):
    rendimiento = datos['Close'].pct_change().mean() * 252
    riesgo = datos['Close'].pct_change().std() * (252 ** 0.5)
    return rendimiento, riesgo

# Configuración de la aplicación
st.title("Simulador Financiero de ETFs - Allianz Patrimonial")
st.write("Esta aplicación permite analizar ETFs y calcular el rendimiento y riesgo para diferentes periodos de tiempo.")

# Selección de ETF y periodo de análisis
etf_seleccionado = st.selectbox("Selecciona el ETF", ("SPY", "QQQ", "DIA", "XLF", "VWO", "XLV", "ITB", "SLV", "EWU", "EWT", "EWY", "EZU", "EWC", "EWJ", "EWG", "EWA", "AGG"))   
periodo_seleccionado = st.selectbox("Selecciona el periodo", ("1mo", "3mo", "6mo", "1y", "3y", "5y", "10y"))

# Obtención de datos
st.write(f"Mostrando datos para el ETF {etf_seleccionado} en el periodo {periodo_seleccionado}.")
datos_etf = obtener_datos_etf(etf_seleccionado, periodo_seleccionado)

# Verificación de que los datos fueron obtenidos
if not datos_etf.empty:
    st.write("### Datos Históricos del ETF")
    st.write(datos_etf.tail())

    # Calcula rendimiento y riesgo
    rendimiento, riesgo = calcular_rendimiento_riesgo(datos_etf)
    st.write(f"*Rendimiento Anualizado:* {rendimiento:.2%}")
    st.write(f"*Riesgo (Desviación Estándar Anualizada):* {riesgo:.2%}")

    # Visualización con Seaborn y Pyplot
    st.write("### Gráfico de Precio de Cierre")
    fig, ax = plt.subplots()
    sns.lineplot(data=datos_etf, x=datos_etf.index, y="Close", ax=ax, color="blue")
    ax.set_title(f"Precio de Cierre de {etf_seleccionado} en {periodo_seleccionado}")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Precio de Cierre (USD)")
    st.pyplot(fig)
else:
    st.write("No se encontraron datos para el ETF seleccionado en el periodo especificado.")


