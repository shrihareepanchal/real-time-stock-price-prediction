# real-time-stock-price-prediction
🌟 Key Features
- **Live Market Data**: 1-minute interval prices from 60+ global exchanges
- **Multi-Model AI Engine**: Simultaneously runs Random Forest, XGBoost, and Linear Regression
- **Smart Alerts**: Push notifications + emails when prices move >$2.00 (configurable)
- **Professional Dashboard**: Institutional-grade candlestick charts with prediction overlays
- **Auto-Retraining**: Models refresh daily with latest market patterns

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
Place firebase_config.json in project root
Enable Cloud Messaging in Firebase Console

🛠 Technical Deep Dive
Data Pipeline:- flowchart TB
    A[Yahoo Finance API] --> 
    B --> C[Feature Engineering]
    C --> D[SMA-10/SMA-50 Calculation]
    D --> E[NaN Handling]
    E --> F[Train/Test Split]

Machine Learning
Model	                    Hyperparameters	  Training Time*	      MSE**
Random Forest	          n_estimators=100	      12.4s	            1.82
XGBoost	                learning_rate=0.1	      9.7s	            1.75
Linear Regression	            -	                0.8s	            2.15

4. Installation (Code Blocks):-
  1. Install dependencies  
      pip install -r requirements.txt

  2. Launch Dashboard:
       streamlit run app.py

📊 Sample Output:-
![Output 1](https://github.com/user-attachments/assets/c58db65b-41a5-4005-a5c9-aa9c6fad8604)
![Output 2](https://github.com/user-attachments/assets/fe145cc3-cc69-40e2-8975-611f49ddb657)
