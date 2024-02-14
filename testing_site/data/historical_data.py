import yfinance as yf

def get_historical_data(ticker, start_date, end_date, interval):
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date, interval=interval)
    return hist


def get_close_price(date, hist):
    return hist.loc[date, 'Close']

