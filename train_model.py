import yfinance as yf
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Fetch stock data
ticker = "AAPL"
stock_data = yf.download(ticker, period="60d", interval="1h", auto_adjust=True)

# Feature Engineering
stock_data['SMA_10'] = stock_data['Close'].rolling(window=10).mean()
stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()

# Define Target: Predict the next closing price
stock_data['Target'] = stock_data['Close'].shift(-1)

# Drop NaN values before splitting
stock_data.dropna(inplace=True)

# Prepare Data
X = stock_data[['SMA_10', 'SMA_50']]
y = stock_data['Target']

# Ensure X and y have the same length
min_length = min(len(X), len(y))
X, y = X.iloc[:min_length], y.iloc[:min_length]

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Train Regression Models
models = {
    "RandomForest": RandomForestRegressor(n_estimators=100, random_state=42),
    "XGBoost": XGBRegressor(n_estimators=100, random_state=42),
    "LinearRegression": LinearRegression()
}

best_model = None
best_score = float("inf")

for name, model in models.items():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f"{name} Metrics:")
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"Mean Absolute Error: {mae:.4f}")
    print(f"R2 Score: {r2:.4f}\n")
    
    if mse < best_score:  # Choose model with lowest error
        best_model = model
        best_score = mse

# Save the Best Model
joblib.dump(best_model, "best_stock_model.pkl")
print(f"Best Model Saved: {best_model}")

# Predict Next Stock Price
if best_model is not None:
    if not X_test.empty:
        predicted_price = best_model.predict(X_test.iloc[-1].values.reshape(1, -1))[0]
        print(f"Predicted Next Price: ${predicted_price:.2f}")
    else:
        print("X_test is empty, cannot make a prediction.")
