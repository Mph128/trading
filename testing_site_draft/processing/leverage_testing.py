from data import historical_data
from processing import analizer as analize
from sympy import symbols, expand, lambdify
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
class LeverageTesting:

    def __init__(self, ticker, interval):
        #symbole of the stock
        self.ticker = ticker
        #time interval for the data, usually 1d
        self.interval = interval
        #historical data for the stock: date, open, high, low, close, volume, dividends, stock splits
        self.hist = historical_data.get_all_historical_data(self.ticker, self.interval)

        #add a col for formatted date
        self.hist['Formatted_Date'] = self.hist.index.strftime('%Y-%m-%d')

        #remove rows that dont have close price
        self.hist = self.hist.dropna(subset=['Close'])

        #start and end date for the stock (default is the entire range of the stock's history)
        self.leverage_start_date = self.hist['Formatted_Date'][0]

        self.start_date = self.hist['Formatted_Date'][0]
        self.end_date = self.hist['Formatted_Date'][-1]

        #close prices for the stock: date, close
        self.close_prices = self.hist[['Formatted_Date','Close']]
        #daily changes in the stock price: date, pct_change
        self.close_prices['Pct_Change'] = self.close_prices['Close'].pct_change()
        # Shift the 'Pct_Change' data up by one row
        self.close_prices['Pct_Change'] = self.close_prices['Pct_Change']

        #leverage for the stock (default is 1)
        self.leverage = 1

        #fees and slippage for the stock (default is 0)
        self.fees = 0
        self.slippage = 0

        #risk free rate for risk calculations (default is 0)
        self.risk_free_rate = 0.03

        #daily changes in the stock price
        self.close_prices['Leveraged_Pct_Change'] = (self.close_prices['Pct_Change'] * self.leverage - self.fees - self.slippage) # if not self.close_prices['Pct_Change'].empty else 0

        #leveraged returns for the stock
        self.leveraged_returns = (self.close_prices['Leveraged_Pct_Change'] + 1).cumprod()

        self.close_prices['Leveraged_Returns'] = (self.leveraged_returns * self.close_prices['Close'][0])

        self.close_prices['Leveraged_Returns'][0] = self.close_prices['Close'][0]

        self.leveraged_changes = self.close_prices['Leveraged_Pct_Change'].dropna()

        self.unleveraged_changes = self.close_prices['Pct_Change'].dropna()

        #remove all rows with NaN values
        self.close_prices = self.close_prices.dropna(subset=['Pct_Change'])

    #test a random set of time ranges to determine optimal leverage
    def test_time_ranges(self, num_tests=100, max_leverage=10):

        #lists to store optimal leverage and sharpe ratios
        optimal_leverages = []
        optimal_sharpe_ratios = []

        def get_random_dates():
             # Generate two random dates within the range
            random_dates = np.random.choice(self.close_prices['Formatted_Date'], 2)

            #order the dates
            random_dates = np.sort(random_dates)

            start_date = random_dates[0]
            end_date = random_dates[1]

            return start_date, end_date

        for i in range(num_tests):
            start_date, end_date = get_random_dates()

            #set the time range
            self.set_time_range(start_date, end_date)

            #get data from test_optimal_leverage
            x_values, return_y_values, optimized_leverage, highest_total_return, sharpe_ratio_y_values, optimized_sharpe_leverage, highest_sharpe_ratio = self.test_optimal_leverage(max_leverage)

            #append the data to the lists
            optimal_leverages.append(optimized_leverage)
            optimal_sharpe_ratios.append(optimized_sharpe_leverage)

        #return the optimal leverages and sharpe ratios
        return optimal_leverages, optimal_sharpe_ratios








    def updateAll(self):
        self.update_leveraged_returns_from_start_date()
        self.update_data_from_time_range()


    def update_leveraged_returns_from_start_date(self):
        self.close_prices = self.hist[['Formatted_Date','Close']][(self.hist['Formatted_Date'] >= self.leverage_start_date)]
        self.close_prices['Pct_Change'] = self.close_prices['Close'].pct_change()
        self.close_prices['Pct_Change'] = self.close_prices['Pct_Change'].shift(-1)
        self.close_prices = self.close_prices.dropna(subset=['Pct_Change'])
        self.close_prices['Leveraged_Pct_Change'] = self.close_prices['Pct_Change'] * self.leverage - self.fees - self.slippage
        self.leveraged_returns = (self.close_prices['Leveraged_Pct_Change'] + 1).cumprod()
        self.close_prices['Leveraged_Returns'] = (self.leveraged_returns * self.close_prices['Close'][0]).shift(1)
        self.close_prices['Leveraged_Returns'][0] = self.close_prices['Close'][0]
        self.update_data_from_time_range()

    #update the data from time range
    def update_data_from_time_range(self):

        # Filter data based on the time range
        mask = ((self.close_prices['Formatted_Date'] >= self.start_date) & (self.close_prices['Formatted_Date'] <= self.end_date))

        # Select data using the mask
        self.leveraged_changes = self.close_prices.loc[mask, 'Leveraged_Pct_Change']
        self.unleveraged_changes = self.close_prices.loc[mask, 'Pct_Change']

        #remove all rows with NaN values
        self.close_prices = self.close_prices.dropna(subset=['Pct_Change'])

    #update the data from new ticker
    def update_data_from_ticker(self, ticker):
        self.ticker = ticker
        self.hist = historical_data.get_all_historical_data(self.ticker, self.interval)
        self.hist['Formatted_Date'] = self.hist.index.strftime('%Y-%m-%d')
        self.hist = self.hist.dropna(subset=['Close'])
        self.leverage_start_date = self.hist['Formatted_Date'][0]
        self.start_date = self.hist['Formatted_Date'][0]
        self.end_date = self.hist['Formatted_Date'][-1]
        self.close_prices = self.hist[['Formatted_Date','Close']]
        self.close_prices['Pct_Change'] = self.close_prices['Close'].pct_change()
        self.close_prices['Pct_Change'] = self.close_prices['Pct_Change'].shift(-1)
        self.close_prices = self.close_prices.dropna(subset=['Pct_Change'])
        self.close_prices['Leveraged_Pct_Change'] = self.close_prices['Pct_Change'] * self.leverage - self.fees - self.slippage
        self.leveraged_returns = (self.close_prices['Leveraged_Pct_Change'] + 1).cumprod()
        self.close_prices['Leveraged_Returns'] = (self.leveraged_returns * self.close_prices['Close'][0]).shift(1)
        self.close_prices['Leveraged_Returns'][0] = self.close_prices['Close'][0]
        self.leveraged_changes = self.close_prices['Leveraged_Pct_Change'].dropna()
        self.unleveraged_changes = self.close_prices['Pct_Change'].dropna()
        self.close_prices = self.close_prices.dropna(subset=['Pct_Change'])
    
    ## LEVERAGED STATISTICS
            #calculate the sharpe ratio for time range
    def get_leveraged_sharpe_ratio(self):
        return analize.sharpe_ratio(self.leveraged_changes, self.risk_free_rate)
    # 'l_sortino_ratio': leverage_data.get_leveraged_sortino_ratio(),
    def get_leveraged_sortino_ratio(self):
        return analize.sortino_ratio(self.leveraged_changes, self.risk_free_rate)
    # 'l_max_drawdown': leverage_data.get_leveraged_max_drawdown(),
    def get_leveraged_max_drawdown(self):
        return analize.max_drawdown(self.leveraged_changes)
    # 'l_annual_return': leverage_data.get_leveraged_annual_return(),
    def get_leveraged_annual_return(self):
        return analize.annual_return(self.leveraged_changes)
    # 'l_annual_volatility': leverage_data.get_leveraged_annual_volatility(),
    def get_leveraged_annual_volatility(self):
        return analize.annual_volatility(self.leveraged_changes)
    # 'l_cumulative_return': leverage_data.get_leveraged_cumulative_return(),
    def get_leveraged_cumulative_return(self):  
        return (analize.cumulative_return(self.leveraged_changes))

    ## UNLEVERAGED STATISTICS
    def get_sharpe_ratio(self):
        return analize.sharpe_ratio(self.unleveraged_changes, self.risk_free_rate)
    #calculate the sortino ratio for time range
    def get_sortino_ratio(self):
        return analize.sortino_ratio(self.unleveraged_changes, self.risk_free_rate) 
    #calculate the maximum drawdown for time range
    def get_max_drawdown(self):
        return analize.max_drawdown(self.unleveraged_changes) 
    #calculate the annual return for time range 
    def get_annual_return(self):
        return analize.annual_return(self.unleveraged_changes)
    #calculate the annual volatility for time range
    def get_annual_volatility(self):
        return analize.annual_volatility(self.unleveraged_changes)
    #calculate the cumulative return for time range
    def get_cumulative_return(self):
        return (analize.cumulative_return(self.unleveraged_changes))

    #getting a specific close price and a hist of close prices
    def get_close_price(self, date):
        return historical_data.get_close_price(date, self.hist)
    def get_close_prices(self):
        return self.close_prices

    #getters and setters for leverage
    def set_leverage(self, leverage):
        self.leverage = leverage
        self.updateAll()

    def get_leverage(self):
        return self.leverage

    def get_hist(self):
        return self.hist
    
    def get_all_formatted_dates(self):
        return self.hist['Formatted_Date']
    
    #getters and setters for risk free rate
    def get_risk_free_rate(self):
        return self.risk_free_rate
    def set_risk_free_rate(self, risk_free_rate):
        self.risk_free_rate = risk_free_rate

    #getters and setters for ticker
    def get_ticker(self):
        return self.ticker.upper()
    def set_ticker(self, ticker):
        self.ticker = ticker
        self.update_data_from_ticker(ticker)
        
    #setters for interval
    def set_leverage_start_date(self, start_date):
        self.leverage_start_date = start_date
        self.update_data_from_time_range()
        
    #setters for start and end dates
    def set_start_date(self, start_date):
        self.start_date = start_date
        self.update_data_from_time_range()
    def set_end_date(self, end_date):
        self.end_date = end_date
        self.update_data_from_time_range()
    def set_time_range(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.update_data_from_time_range()
    def set_time_range_percentage(self, start_percentage, end_percentage):
        self.start_date = self.close_prices['Formatted_Date'][int(len(self.close_prices) * start_percentage/100)]
        self.end_date = self.close_prices['Formatted_Date'][int(len(self.close_prices) * end_percentage/100)-1]
        self.update_data_from_time_range()

    #getters for start and end dates
    def get_start_date(self):   
        return self.start_date
    def get_end_date(self):
        return self.end_date
    def get_time_range(self):
        return self.dates

    #getters for leveraged returns and leveraged cumulative returns
    def get_leveraged_returns(self):
        return self.leveraged_returns
    def get_leveraged_cumulative_returns(self):
        return self.leveraged_cumulative_returns

    #calculating optimal leverage by testing
    def test_optimal_leverage(self, max_leverage=10):
        # Define the leverage values to test
        leverage_values = np.linspace(0, max_leverage, 101).tolist()

        # Initialize the list to store the results
        leverage_results = []
        sharpe_ratio_results = []

        # Iterate over the leverage values
        for leverage in leverage_values:
            # Calculate the leveraged changes
            leveraged_changes = self.unleveraged_changes * leverage

            # Calculate the leveraged returns
            leveraged_returns = (leveraged_changes + 1).cumprod()

            # Calculate the Sharpe ratio
            sharpe_ratio = analize.sharpe_ratio(leveraged_changes, self.risk_free_rate)

            sharpe_ratio_results.append(sharpe_ratio)

            total_return = leveraged_returns[-1]

            # Append the results to the list
            leverage_results.append(total_return)
            
        # returns: leverage values, leverage results, leverage optimized for return, highest total return, sharpe ratio results, leverage optimized for sharpe ratio, highest sharpe ratio
        return leverage_values, leverage_results, leverage_values[leverage_results.index(max(leverage_results))], max(leverage_results), sharpe_ratio_results, leverage_values[sharpe_ratio_results.index(max(sharpe_ratio_results))], max(sharpe_ratio_results)

    def test_sharpe_ratio(self):
        # Define the leverage values to test
        leverage_values = np.linspace(0, 10, 101).tolist()

        # Initialize the list to store the results
        leverage_results = []

        # Iterate over the leverage values
        for leverage in leverage_values:
            # Calculate the leveraged changes
            leveraged_changes = self.unleveraged_changes * leverage

            # Calculate the Sharpe ratio
            sharpe_ratio = analize.sharpe_ratio(leveraged_changes, self.risk_free_rate)

            # Append the results to the list
            leverage_results.append(sharpe_ratio)

        return leverage_values, leverage_results
    # calculate the optimal leverage equation (Not in use...highly inefficient)
    def calculate_leverage_equation(self):
        # Define symbolic variable
        x = symbols('x')

        # Initialize the equation
        eq = 1

        print('Calculating the equation...')
        # Iterate over daily changes and update the equation
        for change in self.unleveraged_changes:
            eq *= (change * x + 1.0)

        print('Converting the equation to a Python function...')
        # Convert the SymPy equation to a Python function
        eq_func = lambda x_val: eq.subs(x, x_val)

        print('Generating values...')
        # Generate x values
        x_values = np.linspace(0, 10, 101).tolist()

        print('X values:')
        print(x_values)
    
        # Calculate y values using the equation
        y_values = np.array([eq_func(x_val) for x_val in x_values]).tolist()

        for i in range(len(y_values)):
            y_values[i] = str(y_values[i])
        print('Y values:')
        print(y_values)

        print('Finding the peaks...')
        # Find the peaks
        peaks, _ = find_peaks(y_values)

        # Print the x values corresponding to the peaks
        print("X values corresponding to peaks:", [x_values[peak] for peak in peaks])

        return x_values, y_values