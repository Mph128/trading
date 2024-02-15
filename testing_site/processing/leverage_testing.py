from data import historical_data
from sympy import symbols, expand
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt
class LeverageTesting:

    def __init__(self, ticker, interval):
        #symbole of the stock
        self.ticker = ticker
        #time interval for the data, usually 1d
        self.interval = interval
        #historical data for the stock: date, open, high, low, close, volume, dividends, stock splits
        self.hist = historical_data.get_all_historical_data(self.ticker, self.interval)

        #close prices for the stock: date, close
        self.close_prices = self.hist['Close']
        #daily changes in the stock price: date, pct_change
        self.daily_changes = self.close_prices.pct_change()

        #start and end date for the stock (default is the entire range of the stock's history)
        self.start_date = self.hist.index[0]
        self.end_date = self.hist.index[-1]

        #leverage for the stock
        self.leverage = 1

        #leveraged returns for the stock
        self.leveraged_returns = self.daily_changes * self.leverage
        #leveraged cumulative returns for the stock(leverage is applied to the *time interval* returns)
        self.leveraged_cumulative_returns = (1 + self.leveraged_returns).cumprod()



    #getting a specific close price and a hist of close prices
    def get_close_price(self, date):
        return historical_data.get_close_price(date, self.hist)
    def get_close_prices(self):
        return self.close_prices
    

    #getters and setters for leverage
    def set_leverage(self, leverage):
        self.leverage = leverage
        self.update_data_from_time_range()

    def get_leverage(self):
        return self.leverage


    #getters and setters for ticker
    def get_ticker(self):
        return self.ticker
    def set_ticker(self, ticker):
        self.ticker = ticker
        self.hist = historical_data.get_all_historical_data(self.ticker, self.interval)
        self.close_prices = self.hist['Close']
        


    #setters for interval
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

    #getters for start and end date
    def get_start_date(self):   
        return self.start_date
    def get_end_date(self):
        return self.end_date
    

    #getters for leveraged returns and leveraged cumulative returns
    def get_leveraged_returns(self):
        return self.leveraged_returns
    def get_leveraged_cumulative_returns(self):
        return self.leveraged_cumulative_returns
    

    #update the leveraged returns and leveraged cumulative returns
    def update_data_from_time_range(self):
        self.close_prices = self.hist.loc[self.start_date:self.end_date, 'Close']
        self.daily_changes = self.close_prices.pct_change()
        self.leveraged_returns = self.daily_changes * self.leverage
        self.leveraged_cumulative_returns = (1 + self.leveraged_returns).cumprod()

    def calculate_leverage_equation(self):

        # Define symbolic variable
        x = symbols('x')

        # Initialize the equation
        eq = 1

        # Iterate over daily changes and update the equation
        for change in self.daily_changes[1:]:
            eq *= (change * x + 1)

        # Convert the SymPy equation to a Python function
        eq_func = lambda x_val: eq.subs(x, x_val)

        # Generate x values
        x_values = np.linspace(0, 25, 1000)

        # Calculate y values using the equation
        y_values = np.array([eq_func(x_val) for x_val in x_values])


        # Find the peaks    # Find peaks
        peaks, _ = find_peaks(y_values)

        # Print the x values corresponding to the peaks
        print("X values corresponding to peaks:", x_values[peaks])

        # Plot the equation and highlight peaks
        plt.plot(x_values, y_values)
        plt.plot(x_values[peaks], y_values[peaks], "x")
        plt.title('Peaks of the Equation')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid(True)
        plt.show()