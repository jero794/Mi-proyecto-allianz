import streamlit as st
import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from etfs_data import ETFs_Data
import numpy as np
from io import BytesIO
from PIL import Image

# Cargar imagen de bienvenida
imagen_bienvenida = Image.open("allianz1.jpg")

# Estado de sesión para gestionar la pantalla de bienvenida
if "mostrar_bienvenida" not in st.session_state:
    st.session_state["mostrar_bienvenida"] = True

# Pantalla de bienvenida
if st.session_state["mostrar_bienvenida"]:
    st.image(imagen_bienvenida, use_column_width=True)  # Muestra la imagen de bienvenida
    if st.button("Quiero Invertir"):
        st.session_state["mostrar_bienvenida"] = False
else:
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
        # Código adicional para ratios financieros...

    # Pestaña 3: Análisis de Precios
    with tab3:
        st.write("### Análisis de Precios")
        # Código adicional para análisis de precios...






