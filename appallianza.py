import streamlit as st
import yfinance as yf
from etfs_data import ETFs_Data  # Asegúrate de que este archivo esté en el mismo directorio

# Título de la aplicación
st.title("Análisis de ETFs")

#### Selector de Datos ####

# Crear un multiselector para elegir múltiples ETFs
etfs_seleccionados = st.multiselect(
    "Selecciona uno o más ETFs para ver los detalles:",
    options=[etf['nombre'] for etf in ETFs_Data],  # Opciones basadas en los nombres de los ETFs
    default=[]
)

# Selector de período de tiempo
periodos = ["1mo", "3mo", "6mo", "1y", "ytd", "3y", "5y", "10y"]
periodo_seleccionado = st.selectbox("Selecciona el período de tiempo:", periodos)

# Función para obtener descripción detallada del ETF
def obtener_descripcion_yf(ticker):
    try:
        # Inicializar el objeto de yfinance para el ETF
        etf = yf.Ticker(ticker)
        
        # Obtener la información completa
        info = etf.info
        
        # Obtener la descripción y otros detalles
        descripcion = info.get("longBusinessSummary", "Descripción no disponible")
        ytd_return = info.get("ytdReturn", "N/A")
        if ytd_return != "N/A":
            ytd_return = round(ytd_return * 100, 2)
        
        dividend_rate = info.get("trailingAnnualDividendRate", "N/A")
        dividend_yield = info.get("trailingAnnualDividendYield", "N/A")
        if dividend_yield != "N/A":
            dividend_yield = round(dividend_yield * 100, 2)
        
        return descripcion, ytd_return, dividend_rate, dividend_yield
    
    except Exception as e:
        return f"Error al obtener la descripción: {e}", "N/A", "N/A", "N/A"

# Mostrar detalles de los ETFs seleccionados si hay al menos uno seleccionado
if etfs_seleccionados:
    st.write("### Detalles de los ETFs Seleccionados:")
    for etf_name in etfs_seleccionados:
        # Buscar en la lista ETFs_Data el diccionario que tenga ese nombre
        etf_info = next((etf for etf in ETFs_Data if etf['nombre'] == etf_name), None)
        if etf_info:
            # Mostrar la información básica del ETF
            st.write(f"**Nombre**: {etf_info['nombre']}")
            st.write(f"**Descripción**: {etf_info['descripcion']}")
            st.write(f"**Símbolo**: {etf_info['simbolo']}")
            
            # Obtener la descripción detallada y métricas del ETF usando `yfinance`
            descripcion, ytd_return, dividend_rate, dividend_yield = obtener_descripcion_yf(etf_info['simbolo'])
            st.write(f"**Descripción detallada**: {descripcion}")
            st.write(f"**Rendimiento YTD**: {ytd_return}%")
            st.write(f"**Tasa de dividendos**: {dividend_rate}")
            st.write(f"**Rendimiento de dividendos**: {dividend_yield}%")
            
            # Descargar y mostrar datos históricos del ETF según el período seleccionado
            datos_historicos = yf.download(etf_info['simbolo'], period=periodo_seleccionado)
            st.write(f"### Datos históricos de {etf_info['simbolo']} ({periodo_seleccionado})")
            st.line_chart(datos_historicos['Close'])
            
            st.markdown("---")  # Línea divisoria entre cada ETF
else:
    st.write("Por favor, selecciona al menos un ETF para ver los detalles.")




