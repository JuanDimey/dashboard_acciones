# Dashboard interactivo con comportamiento histórico de criptos y acciones con análisis técnico

import yfinance as yf
import plotly.graph_objs as go
import streamlit as st
from datetime import datetime
import pandas as pd

# Lista de activos seleccionados
activos = {
    'BTC-USD': 'Bitcoin',
    'ETH-USD': 'Ethereum',
    'LINK-USD': 'Chainlink',
    'SOL-USD': 'Solana',
    'AVAX-USD': 'Avalanche',
    'MATIC-USD': 'Polygon',
    'TAO-USD': 'Bittensor',
    'BABA': 'Alibaba',
    'NU': 'Nubank',
    'NKE': 'Nike',
    'MELI': 'Mercado Libre',
    'AMZN': 'Amazon',
    'TSLA': 'Tesla',
    'NVDA': 'NVIDIA',
    'CSPX.AS': 'CSPX (iShares S&P 500 ETF)',
    'NIO': 'NIO'
}

st.title("📊 Dashboard Interactivo: Seguimiento de Criptos y Acciones")

activo_seleccionado = st.selectbox("Selecciona un activo:", list(activos.keys()), format_func=lambda x: activos[x])

fecha_inicio = st.date_input("Desde:", datetime(2020, 1, 1))
fecha_fin = st.date_input("Hasta:", datetime.now())

if fecha_inicio < fecha_fin:
    with st.spinner('Cargando datos...'):
        data = yf.download(activo_seleccionado, start=fecha_inicio, end=fecha_fin)

    # Calcular medias móviles y RSI
    data['SMA_20'] = data['Close'].rolling(window=20).mean()
    data['SMA_50'] = data['Close'].rolling(window=50).mean()
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    RS = gain / loss
    data['RSI'] = 100 - (100 / (1 + RS))

    # Gráfico principal con medias móviles
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Precio de Cierre'))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_20'], mode='lines', name='Media Móvil 20d'))
    fig.add_trace(go.Scatter(x=data.index, y=data['SMA_50'], mode='lines', name='Media Móvil 50d'))
    fig.update_layout(title=f"Comportamiento histórico de {activos[activo_seleccionado]}",
                      xaxis_title='Fecha',
                      yaxis_title='Precio en USD')
    st.plotly_chart(fig)

    # Gráfico RSI
    fig_rsi = go.Figure()
    fig_rsi.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI'))
    fig_rsi.add_hline(y=70, line_dash='dot', line_color='red')
    fig_rsi.add_hline(y=30, line_dash='dot', line_color='green')
    fig_rsi.update_layout(title='Índice de Fuerza Relativa (RSI)',
                          xaxis_title='Fecha',
                          yaxis_title='RSI')
    st.plotly_chart(fig_rsi)

    # Alertas simples
    st.subheader("🔔 Alertas Técnicas")
    if data['RSI'].iloc[-1] > 70:
        st.warning("RSI por encima de 70: posible sobrecompra.")
    elif data['RSI'].iloc[-1] < 30:
        st.success("RSI por debajo de 30: posible sobreventa.")
    else:
        st.info("RSI en zona neutra.")
else:
    st.warning("La fecha de inicio debe ser anterior a la fecha de fin.")