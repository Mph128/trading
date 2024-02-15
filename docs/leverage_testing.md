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
