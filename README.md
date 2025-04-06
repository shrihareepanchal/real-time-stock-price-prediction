# real-time-stock-price-prediction

The goal of this project is to predict real-time stock prices using Machine Learning or Deep Learning models. The system will fetch live stock data, preprocess it, train a predictive model, and visualize results dynamically.The Real-Time Stock Price Prediction project aims to forecast stock prices dynamically using Machine Learning (ML) and Deep Learning (DL) models. It will fetch live stock data, process it, apply predictive models, and display results on an interactive web interface.

Key Features:-
- Fetch real-time stock price data (Yahoo Finance, Alpha Vantage, or Google Finance API)
- Predict short-term stock price movements using ML/DL models
- Deploy as a web app using Streamlit or Flask
- Visualize real-time predictions using interactive plots
- Zero-cost implementation (free APIs, cloud, or local setup)

Prerequisites
- Python 3.8+
- Gmail account (for alerts)
- Firebase project (optional)

Configuration

    Email Alerts:
    sender_email = "your@gmail.com"
    sender_password = "your-app-password"  # Gmail app password
    receiver_emails = ["trader1@email.com", "trader2@email.com"]

![Email Alert](https://github.com/user-attachments/assets/39ef2e8b-94e6-4cce-8989-295e8e22c2d3)
B[Raw OHLC Data]

Firebase (Optional):
- Place firebase_config.json in project root
- Enable Cloud Messaging in Firebase Console

🛠 Technical Deep Dive
Data Pipeline:- flowchart TB
    A[Yahoo Finance API] --> 
    B --> C[Feature Engineering]
    C --> D[SMA-10/SMA-50 Calculation]
    D --> E[NaN Handling]
    E --> F[Train/Test Split]

Machine Learning

    Model	                  Hyperparameters	   Training Time	    MSE
    Random Forest	          n_estimators=100	      12.4s	            1.82
    XGBoost	                  learning_rate=0.1	      9.7s	            1.75
    Linear Regression	            -	              0.8s	            2.15

4. Installation (Code Blocks):-
   
          1. Install dependencies  
              pip install -r requirements.txt

          2. Launch Dashboard:
              streamlit run app.py

📊 Sample Output:-
![Output 1](https://github.com/user-attachments/assets/c58db65b-41a5-4005-a5c9-aa9c6fad8604)
![Output 2](https://github.com/user-attachments/assets/fe145cc3-cc69-40e2-8975-611f49ddb657)
