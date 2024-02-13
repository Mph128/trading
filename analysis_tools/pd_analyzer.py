# calculate MACD
# default values: macd(12, 26, 9)
# takes in a pandas database of stock data
# returns a dictionary with macd, signal, and the difference between the two
def macd(ticker, period1=12, period2=26, period3=9):
    exp1 = ticker.ewm(span=period1, adjust=False).mean()
    exp2 = ticker.ewm(span=period2, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=period3, adjust=False).mean()
    hist = macd - signal
    return {'macd': macd, 'signal': signal, 'hist': hist}