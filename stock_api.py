import yfinance as yf

def get_current_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d").tail(1)['Close'].values[0]
        return round(price, 2)
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None
