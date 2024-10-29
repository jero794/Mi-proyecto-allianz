import streamlit as st
import yfinance as yf
from etfs_data import ETFs_Data

# Título de la aplicación
st.title("Análisis de ETFs")

#### Selector de Datos ####

# Crear un multiselector usando st.multiselect
etfs_seleccionados = st.multiselect(
    "Selecciona uno o más ETFs para ver los detalles:",
    options=[etf['nombre'] for etf in ETFs_Data],  # Opciones basadas en los nombres de los ETFs
    default=[]  # Por defecto no seleccionamos ninguno
)

# Periodo de tiempo para la consulta de datos
time_periods = ['1mo', '3mo', '6mo', '1y', 'ytd', '3y', '5y', '10y']
selected_period = st.selectbox("Selecciona el periodo de tiempo", time_periods)

# Verificar si hay algún ETF seleccionado
if etfs_seleccionados:
    # Mostrar detalles de los ETFs seleccionados
    st.write("### Detalles de los ETFs Seleccionados:")
    for etf_name in etfs_seleccionados:
        # Buscar en la lista ETFs_Data el diccionario que tenga ese nombre
        etf_info = next((etf for etf in ETFs_Data if etf['nombre'] == etf_name), None)
        if etf_info:
            # Mostrar la información del ETF seleccionado
            st.write(f"**Nombre**: {etf_info['nombre']}")
            st.write(f"**Descripción**: {etf_info['descripcion']}")
            st.write(f"**Símbolo**: {etf_info['simbolo']}")
            
            # Descargar y mostrar datos históricos del ETF
            data = yf.download(tickers=etf_info['simbolo'], period=selected_period)
            if not data.empty:
                st.write(f"### Datos históricos para {etf_info['nombre']} - {selected_period}")
                st.line_chart(data['Close'])  # Gráfico de cierre del ETF
            else:
                st.write("No hay datos disponibles para este periodo.")
            
            st.markdown("---")  # Línea divisoria entre cada ETF
else:
    st.write("Por favor, selecciona al menos un ETF para ver los detalles.")




