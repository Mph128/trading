import numpy as np
import pandas as pd
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

def sharpe_ratio(returns, risk_free_rate):
    excess_return = np.mean(returns) - risk_free_rate
    std_dev = np.std(returns)
    return excess_return / std_dev

def sortino_ratio(portfolio_returns, risk_free_rate):
    downside_returns = [r for r in portfolio_returns if r < risk_free_rate]
    downside_deviation = np.std(downside_returns, ddof=1) if len(downside_returns) > 0 else 0
    portfolio_return = np.mean(portfolio_returns)
    sortino_ratio = (portfolio_return - risk_free_rate) / downside_deviation if downside_deviation != 0 else np.nan
    return sortino_ratio

def max_drawdown(portfolio_returns):
    cumulative_returns = np.cumprod(1 + portfolio_returns)
    cumulative_max = np.maximum.accumulate(cumulative_returns)
    drawdowns = (cumulative_max - cumulative_returns) / cumulative_max
    max_drawdown = np.max(drawdowns)
    return max_drawdown