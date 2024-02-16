# Algo Trading

The primary goal of this project is to create a custom research tool for backtesting possible strategies in the stock market. The long term goal is to develop a trading bot that will determine when to buy and sell stocks based off of live market data. 


## Leverage Testing

### Problem: 

The prevailing view suggests that leveraged Exchange-Traded Funds (ETFs) are not suitable for long-term "buy and hold" strategies. This is primarily due to their high fees, often exceeding 1%, and the concept of volatility decay. Leveraged ETFs typically rebalance daily, which means while they magnify daily index returns, they do not necessarily provide a similar multiple over the long term, like annual returns. As leverage increases, volatility decay tends to worsen, further diminishing potential returns.

While it's generally acknowledged that leveraged ETFs are not ideal for long-term investments due to high fees and volatility decay, there could be scenarios where an optimal amount of leverage might yield favorable results.

If an investor manages to identify an optimal level of leverage that minimizes the impact of fees and volatility decay while maximizing returns, it's possible to mitigate the drawbacks associated with leveraged ETFs. However, finding this optimal leverage level requires extensive analysis, understanding of market conditions, and risk management strategies.

### Goal:

#### The overall objective is to develop a comprehensive leverage testing software that empowers users to make informed decisions regarding the optimal amount of leverage to employ in their investment strategies. Through customizable analysis of leverage levels across different time frames, the software aims to enhance investment performance, mitigate risks, and maximize returns

Select an amount of leverage to use: This objective is crucial because it allows users to determine the level of leverage they want to apply to their investments. Different investors have different risk tolerances and investment goals, so being able to select an appropriate amount of leverage tailored to their individual preferences is essential for optimizing their investment strategy and managing risk effectively.

Select a time frame to test: Time frame selection is important because it enables users to evaluate the performance of their leveraged investments over specific periods. Different investment strategies may perform differently over various time frames, so being able to test and analyze performance over different durations helps investors gain insights into the effectiveness of their strategies and adapt them accordingly.

Compare different amounts of leverage over the same timeframe: This objective allows users to conduct comparative analyses to determine the impact of varying levels of leverage on investment returns and risk. By comparing different leverage ratios side by side over the same time frame, investors can assess the trade-offs between risk and potential returns associated with each level of leverage and make informed decisions about their investment strategies.

Compare different time frames with the same amount of leverage: Comparing different time frames with consistent levels of leverage helps users understand how the performance of leveraged investments varies across different market conditions and economic cycles. This analysis can provide valuable insights into the robustness and consistency of investment strategies under various market conditions, helping investors identify optimal time frames for leveraging their investments effectively.

Graph the output: Graphical representation of the output is essential for visualizing and interpreting the results of leverage testing. Graphs allow users to easily identify trends, patterns, and relationships in the data, making it easier to draw conclusions and make informed decisions. Visualizations such as line charts, bar charts, and scatter plots can effectively illustrate the performance of leveraged investments over different time frames and leverage levels, enhancing the clarity and understanding of the analysis results.

Identify the optimal leverage level: Determine the leverage level that maximizes the desired investment objective for the specific time range. This could involve selecting the leverage level with the highest risk-adjusted returns, the lowest drawdowns, or a combination of factors tailored to the investor's preferences and risk tolerance.



### A brief rundown of some of the python libraries being used in the project:

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

## Flask
Flask is a web framework for Python used to build web applications. It provides tools and libraries for handling web requests, routing URLs to functions, and generating HTML content dynamically.

## Chart.js
Chart.js is a JavaScript library for creating interactive charts and graphs on web pages. It provides a simple yet powerful API for generating various types of charts, including line charts, bar charts, pie charts, and more.

## SymPy
SymPy is a Python library for symbolic mathematics. It provides tools for working with symbolic expressions, equations, and algebraic computations.

## NumPy
NumPy is a Python library for numerical computing. It provides support for large, multi-dimensional arrays and matrices, along with a collection of mathematical functions to operate on these arrays.

## SciPy
SciPy is a Python library for scientific computing and technical computing. It provides modules for optimization, integration, interpolation, linear algebra, and more.

---





TBC
