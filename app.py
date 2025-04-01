import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import joblib
import time
import os
import plotly.graph_objects as go
import firebase_admin
from firebase_admin import messaging, credentials
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load Firebase Credentials
firebase_config_path = "firebase_config.json"
if os.path.exists(firebase_config_path) and not firebase_admin._apps:
    cred = credentials.Certificate(firebase_config_path)
    firebase_admin.initialize_app(cred)

# Function to send Firebase notification
def send_firebase_notification(title, body):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        topic="stock_alerts"
    )
    messaging.send(message)

# Function to send email alert
def send_email_alert(subject, body):
    sender_email = "shriharee004@gmail.com"
    sender_password = "jomo ebkm hyoz tedv"  # Use App Password for security
    receiver_emails = ["shriharee0004@gmail.com"]  # List of traders

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        for recipient in receiver_emails:
            msg["To"] = recipient
            server.sendmail(sender_email, recipient, msg.as_string())
        server.quit()
        print("✅ Email alerts sent to all traders!")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Load Trained Model
model_path = "best_stock_model.pkl"
model = joblib.load(model_path)

# Function to fetch Real-Time Stock Data (Cached for Optimization)
@st.cache_data(ttl=60)
def get_latest_stock_data(ticker):
    try:
        stock_data = yf.download(ticker, period="1d", interval="1m")
        if stock_data.empty:
            st.error(f"No stock data found for {ticker}. Check the symbol.")
            return pd.DataFrame()
        return stock_data
    except Exception as e:
        st.error(f"Error fetching stock data: {e}")
        return pd.DataFrame()

# Streamlit UI
st.title("📈Real-Time Stock Price Prediction")
ticker = st.text_input("Enter Stock Symbol", "AAPL")

if st.button("Start Predicting"):
    while True:
        stock_data = get_latest_stock_data(ticker)

        if stock_data.empty:
            st.error("Stock data is empty. Try again later.")
            break

        latest_close_price = stock_data['Close'].iloc[-1]
        latest_volume = stock_data['Volume'].iloc[-1]
        
        features = np.array([[latest_close_price, latest_volume]]).reshape(1, -1)
        predicted_price = model.predict(features)[0]

        st.write(f"**Current Price:** ${latest_close_price.iloc[-1]:.2f}")
        st.write(f"**Predicted Next Price:** ${predicted_price:.2f}")

        # Alert if price changes significantly
        price_diff = abs(predicted_price - latest_close_price)
        if price_diff.iloc[-1] > 2:
            alert_message = f"⚠️ Stock {ticker} changed by ${price_diff.iloc[-1]:.2f}!"
            st.warning(alert_message)
            send_firebase_notification("Stock Alert", alert_message)
            send_email_alert(f"Stock Alert: {ticker}", alert_message)

        # Plot stock price trend
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=[pd.Timestamp.now()], y=[latest_close_price], mode="lines+markers", name="Actual Price", line=dict(color="blue", width=2)))
        fig.add_trace(go.Scatter(x=[pd.Timestamp.now()], y=[predicted_price], mode="lines", name="Predicted Price", line=dict(color="red", width=2, dash="dash")))
        fig.update_layout(title=f"📈 Stock Price Trend for {ticker}", xaxis_title="Timestamp", yaxis_title="Stock Price (USD)", template="plotly_dark", height=500)
        st.plotly_chart(fig, use_container_width=True)

        # Auto-refresh every 30 seconds
        time.sleep(30)
        