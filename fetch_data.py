import yfinance as yf

def fetch_stock_data(ticker):
    stock_data = yf.download(ticker, period="60d", interval="1h")
    return stock_data

if __name__ == "__main__":
    ticker = "AAPL"
    data = fetch_stock_data(ticker)
    print(data.tail())
