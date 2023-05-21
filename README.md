# Algo Trading

The goal of this project is to create a trading bot that will determine when to buy and sell stocks based off of live market data. 

### First, a brief rundown of the python libraries being used in the project:

---

## yfinance
the yfinance API provides a way to access past and present market data for stocks and cryptocurrencies. 

One benefit is yfinance provides high granularity of data. The full range of intervals available are:
```
1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
```
Note that the 1m data is only retrievable for the last 7 days, and anything intraday (interval <1d) only for the last 60 days.

### Scope

yfinance will mostly be used for prototyping. In future, a more reliable system will need to be implemented. A service providing low latency data directly from exchanges such as Polygon or IEX will likely be used in future implementations.

---

TBC