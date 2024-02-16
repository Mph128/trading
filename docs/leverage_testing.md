# Leverage Testing

### The goal of leverage testing is to find the optimal amount of leverage (daily leverage) to trade with of certain timeframes. To achieve this I will implement a website with easy UI to backtest strategies.
---
### Requirements

1. select an amount of leverage to use
2. select a time frame to test
3. compare different amounts of leverage over the same timeframe
4. compare different timeframes with same amount of leverage
5. graph the output

---
## Issues:

### Runtime to find optimal leverage

Strategy: 

Get a system of linear equations representing the effect of leverage on the stock price. In this case leverage amount is on the x-axis and %return is on the y-axis. 

Next we can multiply these equations together to get a higher order equation that represents the effects of leverage on the total percent return achieved.

```
def calculate_leverage_equation(self):

    # Define symbolic variable
    x = symbols('x')

    # Initialize the equation
    eq = 1

    # Iterate over daily changes and update the equation
    for change in self.daily_changes[1:]:
        eq *= (change * x + 1)
```

We can then graph this equation and find the local maxima in a specified range. From figure 1 we can see that the return of SPY from 1994-10-01 to 2023-12-31 at 1x leverage was about 17.5x. This makes sense as this averages out to about a 10% gain each year. We also find that using 3.1x *daily* leverage would more than 10x those returns over the same period. 

*This is before fees are taken into account*

![SPY leverage analysis from 1994-10-01 to 2023-12-31](/images/Figure_1.png) *Figure 1: SPY leverage analysis from 1994-10-01 to 2023-12-31*

The problem with this approach is that it requires a ton of processing time and is highly impractical for a lighweight research tool. 

### Possible solutions:

1. Use numpy arrays to speed up matrix multiplication

2. look into functional programming languages such as hascal, might be more intuitive to approach this problem, although may not be more efficient

3. maximum leverage k is approximated by the following formula (for small amounts of leverage):
k = μ / σ2
Where μ is the mean daily return of the market or index, and σ is the volatility of the market or index (defined as the standard deviation of μ).

source: Alpha Generation and Risk Smoothing using Managed Volatility


---

# Ideas

## Calculate risk

It would be good to calculate and provide **Max Drawdown, Sharpe Ratio, Sortino Ratio, CAGR, STDEV** 

#### Sharpe Ratio
To calculate Sharpe ratio I will use the average of the 10 year treasury rate over the selected time period. 

Sharpe Ratio = (R<sub>p</sub> - R<sub>f</sub>) / σ<sub>p</sub>

Where:

- R<sub>p</sub> is the expected return of the investment.
- R<sub>f</sub> is the risk-free rate.
- σ<sub>p</sub> is the standard deviation of the investment's returns.

#### Max Drawdown

Max Drawdown = (Peak Value - Trough Value) / Peak Value

Where:

- "Peak Value" is the highest value of the asset within the period being analyzed.
- "Trough Value" is the lowest value of the asset following the peak value.
- The result is expressed as a percentage.

#### Sortino Ratio

The Sortino ratio is useful because it penalizes only downside volatility, unlike the Sharpe ratio, which penalizes both upside and downside volatility. Again, I will use the average 10 year treasury yield as the risk-free rate.
 
Sortino_Ratio = (Portfolio_Return - Risk_Free_Rate) / Downside_Deviation

- Portfolio Return is the return of the investment portfolio.
- Risk-Free Rate is the risk-free rate of return, typically the return on a Treasury bill or similar investment.
- Downside Deviation is the standard deviation of negative returns or downside volatility.

#### CAGR
CAGR (Compound Annual Growth Rate): CAGR is a measure of the annual growth rate of an investment over a specified period of time. It represents the geometric progression ratio that provides a constant rate of return over the investment's time horizon, assuming the investment's value increases or decreases at a steady rate each year. CAGR smooths out fluctuations in the investment's value over time and is commonly used to evaluate the performance of investments like stocks, mutual funds, or portfolios over multiple years.

#### Standard Deviation
Standard Deviation of Stock Prices: Standard deviation measures the dispersion or variability of a set of values from their mean (average). When applied to stock prices, it quantifies the extent of price fluctuations around the average price over a specific period of time. A higher standard deviation indicates greater volatility, implying larger price swings, while a lower standard deviation suggests more stable prices. Investors often use standard deviation as a measure of risk, with higher values indicating riskier investments.

## Dollar cost Averaging

Leveraged positions are inherently more sensitive to market volatility. Dollar-cost averaging can help mitigate the impact of short-term market fluctuations by spreading out the investment over time, potentially reducing the volatility associated with the leveraged position.

DCA can be used as a risk management tool when employing leverage. By investing a fixed amount of money at regular intervals, investors may mitigate the risk associated with timing the market or making a large, lump-sum leveraged investment at an inopportune time.

## Fees

Obviously leveraged ETFs come at a cost. Due to fees, and potential tracking errors, LETFs may achieve a return slightly lower than expected. When simulating returns it is important to take this into account.

---
# Great Sources:

https://www.afrugaldoctor.com/home/leveraged-etfs-and-volatility-decay-part-2

Alpha Generation and Risk Smoothing Using Managed Volatility: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1664823