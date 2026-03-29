# ================================================
# Dashboard Financier Canadien
# ================================================

import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

# ---- TITRE ----
st.title("Dashboard actions canadiennes")
st.write("Analyse en temps réel des actions canadiennes")

# ---- ENTRÉE UTILISATEUR ----
symbol = st.text_input("Action 1 (ex: RY, TD, SHOP)", "RY")
period = st.selectbox("Période action 1", ["1mo", "3mo", "6mo", "1y", "2y"])

symbol_2 = st.text_input("Action 2 (ex: TD, SHOP, CNR)", "TD")
period_2 = st.selectbox("Période action 2", ["1mo", "3mo", "6mo", "1y", "2y"])

# ---- TÉLÉCHARGER LES DONNÉES ----
data = yf.download(symbol, period=period)
data_2 = yf.download(symbol_2, period=period_2)

if len(data) > 0 and len(data_2) > 0:

    # ---- CALCULS ACTION 1 ----
    prix_actuel = float(data['Close'].iloc[-1])
    prix_debut = float(data['Close'].iloc[0])
    rendement = float(((prix_actuel - prix_debut) / prix_debut) * 100)
    volatilite = float(data['Close'].pct_change().std() * 100)

    # ---- CALCULS ACTION 2 ----
    prix_actuel_2 = float(data_2['Close'].iloc[-1])
    prix_debut_2 = float(data_2['Close'].iloc[0])
    rendement_2 = float(((prix_actuel_2 - prix_debut_2) / prix_debut_2) * 100)
    volatilite_2 = float(data_2['Close'].pct_change().std() * 100)

    # ---- SIGNAL ACTION 1 ----
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()

    if float(data['MA50'].iloc[-1]) > float(data['MA200'].iloc[-1]):
        signal = ":) ACHAT"
    else:
        signal = ":( VENTE"

    # ---- SIGNAL ACTION 2 ----
    data_2['MA50'] = data_2['Close'].rolling(window=50).mean()
    data_2['MA200'] = data_2['Close'].rolling(window=200).mean()

    if float(data_2['MA50'].iloc[-1]) > float(data_2['MA200'].iloc[-1]):
        signal_2 = ":)ACHAT"
    else:
        signal_2 = ":( VENTE"

    # ---- MÉTRIQUES ACTION 1 ----
    st.subheader(f" {symbol}")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Prix actuel", f"${prix_actuel:.2f}")
    col2.metric("Rendement", f"{rendement:.2f}%")
    col3.metric("Volatilité", f"{volatilite:.2f}%")
    col4.metric("Signal", signal)

    # ---- MÉTRIQUES ACTION 2 ----
    st.subheader(f" {symbol_2}")
    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Prix actuel", f"${prix_actuel_2:.2f}")
    col6.metric("Rendement", f"{rendement_2:.2f}%")
    col7.metric("Volatilité", f"{volatilite_2:.2f}%")
    col8.metric("Signal", signal_2)

    # ---- GRAPHIQUE ----
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data['Close'], label=symbol, color='blue')
    ax.plot(data_2['Close'], label=symbol_2, color='green')
    ax.plot(data['MA50'], label=f'MA50 {symbol}', color='orange')
    ax.plot(data['MA200'], label=f'MA200 {symbol}', color='red')
    ax.set_title(f"Comparaison {symbol} vs {symbol_2}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Prix ($)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

else:
    st.error("Symbole invalide — essaie RY, TD, SHOP, CNR")
