import numpy as np
import pandas as pd

def get_daily_risk_free_rate(annual_risk_free_rate):
    # based off of 10 year treasury yield
    daily_rate = (1 + annual_risk_free_rate)**(1/252) - 1
    return daily_rate

def sharpe_ratio1(returns, risk_free_rate):
    annualized = annual_return(returns)
    print('annualized1: ',annualized)
    excess_return = annualized - risk_free_rate
    print('excess_return1: ',excess_return)
    std_dev = np.std(returns) * np.sqrt(252)
    print('std_dev1: ',std_dev)
    return excess_return / std_dev

def sharpe_ratio(returns, risk_free_rate):
    average_return = np.mean(returns)
    print('average_return2: ',average_return)
    excess_return = average_return - get_daily_risk_free_rate(risk_free_rate)
    print('excess_return2: ',excess_return)
    std_dev = np.std(returns)
    print('std_dev2: ',std_dev * np.sqrt(252))
    return excess_return / std_dev * np.sqrt(252)

def sortino_ratio(portfolio_returns, risk_free_rate):
    downside_returns = [r for r in portfolio_returns if r < 0]
    # print('downside_returns: ',downside_returns)
    downside_deviation = np.std(downside_returns, ddof=1)*np.sqrt(252) if len(downside_returns) > 0 else 0
    # print('downside_deviation: ',downside_deviation)
    portfolio_return = annual_return(portfolio_returns)
    # print('portfolio_return: ',portfolio_return)
    sortino_ratio = (portfolio_return - risk_free_rate) / downside_deviation if downside_deviation > 0 else 0
    # print('sortino_ratio: ',sortino_ratio)
    return sortino_ratio

def max_drawdown(portfolio_returns):
    cumulative_returns = np.cumprod(portfolio_returns)
    cumulative_max = np.maximum.accumulate(cumulative_returns)
    drawdowns = (cumulative_max - cumulative_returns) / cumulative_max
    max_drawdown = np.max(drawdowns)
    return max_drawdown

def annual_return(portfolio_returns):
    cumulative_returns = np.cumprod(1+portfolio_returns)
    print('cumulative_returns1: ',cumulative_returns)
    years = len(portfolio_returns) / 252
    print('years: ',years)
    print('average daily return: ',(cumulative_returns[-1])**(1/(years*252)) - 1)
    return (cumulative_returns[-1])**(1/years) - 1

def annual_volatility(portfolio_returns):
    return np.std(portfolio_returns) * np.sqrt(252)

def cumulative_return(portfolio_returns):
    return np.prod(portfolio_returns + 1) - 1