import yfinance as yf
import streamlit as st


def obtener_descripcion_yf(ticker):
    try:
        # Inicializar el objeto de yfinance para el ETF
        etf = yf.Ticker(ticker)

        # Obtener la información completa
        info = etf.info

        # Obtener la descripción del ETF
        descripcion = info.get("longBusinessSummary", "Descripción no disponible")

        # Obtener el rendimiento YTD y convertir a porcentaje
        ytd_return = info.get("ytdReturn", None)
        if ytd_return is not None:
            ytd_return = round(ytd_return * 100, 2)
        else:
            ytd_return = "N/A"

        # Obtener los dividendos anuales por acción
        dividend_rate = info.get("trailingAnnualDividendRate", None)
        if dividend_rate is None:
            dividend_rate = "N/A"

        # Obtener el rendimiento anual de dividendos y convertir a porcentaje
        dividend_yield = info.get("trailingAnnualDividendYield", None)
        if dividend_yield is not None:
            dividend_yield = round(dividend_yield * 100, 2)
        else:
            dividend_yield = "N/A"

        # Devolver la descripción, YTD, tasa de dividendos y rendimiento de dividendos
        return descripcion, ytd_return, dividend_rate, dividend_yield

    except Exception as e:
        return f"Error al obtener la descripción: {e}", "N/A", "N/A", "N/A"