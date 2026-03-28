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
symbol = st.text_input("Entre le symbole d'une action (ex: RY, TD, SHOP)", "RY")
period = st.selectbox("Période d'analyse", ["1mo", "3mo", "6mo", "1y", "2y"])

# ---- TÉLÉCHARGER LES DONNÉES ----
data = yf.download(symbol, period=period)

if len(data) > 0:

    # ---- CALCULS ----
    prix_actuel = float(data['Close'].iloc[-1])
    prix_debut = float(data['Close'].iloc[0])
    rendement = float(((prix_actuel - prix_debut) / prix_debut) * 100)
    volatilite = float(data['Close'].pct_change().std() * 100)

    # ---- SIGNAL ----
    data['MA50'] = data['Close'].rolling(window=50).mean()
    data['MA200'] = data['Close'].rolling(window=200).mean()

    if float(data['MA50'].iloc[-1]) > float(data['MA200'].iloc[-1]):
        signal = "ACHAT"
    else:
        signal = "VENTE"

    # ---- MÉTRIQUES ----
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Prix actuel", f"${prix_actuel:.2f}")
    col2.metric("Rendement", f"{rendement:.2f}%")
    col3.metric("Volatilité", f"{volatilite:.2f}%")
    col4.metric("Signal", signal)

    # ---- GRAPHIQUE ----
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(data['Close'], label='Prix', color='blue')
    ax.plot(data['MA50'], label='MA 50 jours', color='orange')
    ax.plot(data['MA200'], label='MA 200 jours', color='red')
    ax.set_title(f"Analyse de {symbol}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Prix ($)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

else:
    st.error("Symbole invalide — essaie RY, TD, SHOP, CNR")

