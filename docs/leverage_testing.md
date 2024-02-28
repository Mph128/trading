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

### Overall Efficiency

I have not spent any time streamlining the site. It is a heavyweight draft of what it could be. As such, efficiency is some low hanging fruit for improvement. I will try to balance making things run more smoothly and efficiently with creating new tools and features.

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

4. Just test the differenct amuonts of leverage. I am only plotting maybe 50-100 datapoints so running a test that many times will not b nearly as hard nor will it scale as quickly as trying to find the actual equation. This is the approach i will implement 

    *Note: after timing different approaches this seems to come out ahead and will serve the scope of these tests.*


---

# Ideas

## MACD Strategy to Reduce Volatility

MACD can be used to filter out trades during choppy or ranging market conditions, focusing only on trades that align with the prevailing trend. By avoiding trades in volatile sideways markets, this approach can potentially reduce the overall volatility of returns. Maybe combine MACD with other indicators or filters that aim to reduce volatility or smooth price movements. For example, using MACD in conjunction with a moving average crossover strategy can provide additional confirmation signals and potentially reduce false signals, thereby decreasing overall volatility. This could increase the saftey of using leverage

## Dollar cost Averaging

Leveraged positions are inherently more sensitive to market volatility. Dollar-cost averaging can help mitigate the impact of short-term market fluctuations by spreading out the investment over time, potentially reducing the volatility associated with the leveraged position.

DCA can be used as a risk management tool when employing leverage. By investing a fixed amount of money at regular intervals, investors may mitigate the risk associated with timing the market or making a large, lump-sum leveraged investment at an inopportune time.

## Fees

Obviously leveraged ETFs come at a cost. Due to fees, and potential tracking errors, LETFs may achieve a return slightly lower than expected. When simulating returns it is important to take this into account.

## Finding optimal leverage over a time range

To find a level of leverage that could be recommended, it woul be important to test how leverage holds up over different time ranges throughout history. 

### Implementation 1

The first idea is to generate random time ranges and find the optimal leverage for that range. We can do this for a certain number of time ranges, say 1000, and get a histogram of the optimal leverages. I wrote some code that generated 1000 random time ranges (of varying lengths) of SPY and calculated and graphed the optimal leverage for each range. I optimized for sharpe ratio and for returns so there were 2 graphs (shown below)

![returns ](/images/optimalleveragesforreturns.png) *Figure 2: Leverage optimized for returns*

![sharpe ratio](/images/optimalleveragesforsharperatios.png) *Figure 3: Leverage optimized for Sharpe ratio*

The 0 and 8 bins have a high frequency of occurance simply because they represent all leverages below 0 and above 8 respectivly. 

One issue with this approach is that data in the middle of the full time range available for analysis will likely be oversampled and data at either end of the range will be undersampled. For example: SPY data runs from 1993 to 2024 so if we sample 2 random dates the likelyhood that 2005 will be in the sampled date range will be higher than the likelyhood 1993 will be in the date range. This means that data from 2005 will have a higher impact on our histogram data.

### Implementation 2

The idea for implementation 2 is that we can sample time ranges of a se interval. This will still have a little bias for data from from the middle of the full time range, bu should be better if the interval is small enough, say 2 years. Unfortunatly, for investors with a time horizon of longer than 2 years, this data may be less useful. 

### Implementation 3

To make the tool perhapse more useful to longer term investors we can try to show a trend for how daily leverage effects expected return as we increase time in the market. maybe we can start sampling time ranges of 2 years, plot that data, then increase time range increment to 3 years and plot the data next to it. We should be able to see what happens to the mean, standard deviation, and skewness of the bell curve as we increase the time range interval.

---
# Implemented

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


---
# Great Sources:

https://www.afrugaldoctor.com/home/leveraged-etfs-and-volatility-decay-part-2

Alpha Generation and Risk Smoothing Using Managed Volatility: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1664823
