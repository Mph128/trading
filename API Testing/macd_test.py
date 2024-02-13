import yfinance as yf
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt

wallet = 100
buy_price = 0
sell_price = 0


msft = yf.Ticker("MSFT")

# get stock info
msft.info

# get historical market data

# this is optional, default is None
# start: 'YYYY-MM-DD', end: 'YYYY-MM-DD'
period = "3mo"
interval = "1d"
hist = msft.history(period=period, interval=interval)
# print(hist['Close'])


# calculate MACD
# default values: macd(12, 26, 9)
# takes in a pandas database of stock data
# returns a dictionary with macd, signal, and the difference between the two
def macd(ticker, period1=12, period2=26, period3=9):
    exp1 = ticker.ewm(span=period1, adjust=False).mean()
    exp2 = ticker.ewm(span=period2, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=period3, adjust=False).mean()
    diff = macd - signal
    return diff.to_frame().append([macd.to_frame(), signal.to_frame()])
# calculate MACD
macd_table = macd(hist['Close'])

# print(macd_dict['macd'])
# print(macd_dict['signal'])
# print(macd_dict['hist'])


# plot MACD
macd_table['macd'].plot(label='MACD', color='g')
ax = macd_table['signal'].plot(label='Signal Line', color='r')
macd_table['diff'].plot(label='MACD - Signal', color='b')
hist['Close'].plot(ax=ax, secondary_y=True, label='Stock Price')
ax.set_ylabel('MACD')
ax.right_ax.set_ylabel('Price $')
ax.set_xlabel('Date')
lines = ax.get_lines() + ax.right_ax.get_lines()
ax.legend(lines, [l.get_label() for l in lines], loc='upper left')
plt.show()




