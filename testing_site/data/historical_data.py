import yfinance as yf



def get_range_historical_data(ticker, start_date, end_date, interval):
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start_date, end=end_date, interval=interval)
    return hist

def get_all_historical_data(ticker, interval):
    stock = yf.Ticker(ticker)
    hist = stock.history(period='max', interval=interval)
    return hist

def get_close_price(date, hist):
    return hist.loc[date, 'Close']

def get_close_prices(hist, start_date, end_date):
    close_hist = hist['Close'] 
    return close_hist[start_date:end_date]

