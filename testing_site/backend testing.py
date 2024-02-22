from processing import leverage_testing as ltest
from data import historical_data
import time
lt = ltest.LeverageTesting('spy', '1d')
# print(lt.get_close_prices())
# lt.set_time_range('1994-10-01', '2023-12-31')
# print(lt.get_close_prices())
# Start the timer
# start_time = time.time()
# lt.calculate_leverage_equation()
# # End the timer
# end_time = time.time()

# Calculate the elapsed time
# elapsed_time = end_time - start_time

# print (lt.leveraged_cumulative_returns)

# # Print the elapsed time
# print("Elapsed time:", elapsed_time, "seconds")


# print ("Close Prices:", lt.close_prices)
print("sharpe ratio 1: " ,lt.get_sharpe_ratio1())
print("sharpe ratio 2: " ,lt.get_sharpe_ratio2())
# print("sortino ratio: ", lt.get_sortino_ratio())
# print("max drawdown: ", lt.get_max_drawdown())
# print("annual return: ", lt.get_annual_return())
# print("annual volatility: ", lt.get_annual_volatility())
# print("cumulative return: ", lt.get_cumulative_return())

