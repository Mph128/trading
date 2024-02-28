from processing import leverage_testing as ltest
from data import historical_data
import time
import matplotlib.pyplot as plt

lt = ltest.LeverageTesting('spy', '1d')

## Testing the time range

# lt.set_time_range('2004-10-01', '2010-11-01')
# print('start date: ', lt.get_start_date())
# print('end date: ', lt.get_end_date())


################################################################
## Testing the statistics

# print('Leveraged Statistics')
# print("sharpe ratio: " ,lt.get_leveraged_sharpe_ratio())
# print("sortino ratio: ", lt.get_leveraged_sortino_ratio())
# print("max drawdown: ", lt.get_leveraged_max_drawdown())
# print("annual return: ", lt.get_leveraged_annual_return())
# print("annual volatility: ", lt.get_leveraged_annual_volatility())
# print("cumulative return: ", lt.get_leveraged_cumulative_return())
# print('Unleveraged Statistics')
# print("sharpe ratio: " ,lt.get_sharpe_ratio())
# print("sortino ratio: ", lt.get_sortino_ratio())
# print("max drawdown: ", lt.get_max_drawdown())
# print("annual return: ", lt.get_annual_return())
# print("annual volatility: ", lt.get_annual_volatility())
# print("cumulative return: ", lt.get_cumulative_return())


################################################################
## Testing the leverage equations

# equation_times = []
# test_times = []

# lt.set_end_date('2015-01-01')

# for i in range(20):
#     start_date = str(1995 + i) + '-01-01'
#     lt.set_start_date(start_date)

#     # #start timer
#     # start_time = time.time()

#     # #calculate leverage equation
#     # x_vals, y_vals = lt.calculate_leverage_equation()

#     # #stop timer
#     # stop_time = time.time()

#     # equation_times.append(stop_time - start_time)

#     #start timer
#     start_time = time.time()

#     #test for leverage data
#     x_vals, y_vals = lt.test_optimal_leverage()

#     #stop timer
#     stop_time = time.time()

#     test_times.append(stop_time - start_time)

# # print('Equation Times:', equation_times)
# print('Test Times:', test_times)

# # plt.plot(equation_times, label='Equation Times')
# plt.plot(test_times, label='Test Times')
# plt.legend()
# plt.show()


################################################################
## Testing random leverage
num_tests = 1000
max_leverage = 8

optimal_leverages, optimal_sharpe_ratios = lt.test_time_ranges(num_tests=num_tests, max_leverage=max_leverage)

# Plotting the optimal leverages
plt.figure(figsize=(10, 5))
plt.hist(optimal_leverages, bins=max_leverage*5, color='blue', edgecolor='black')
plt.title('Histogram of Optimal Leverages')
plt.xlabel('Optimal Leverages')
plt.ylabel('Frequency')
plt.show()

# Plotting the optimal sharpe ratios
plt.figure(figsize=(10, 5))
plt.hist(optimal_sharpe_ratios, max_leverage*5, color='green', edgecolor='black')
plt.title('Histogram of Optimal Sharpe Ratios')
plt.xlabel('Optimal Sharpe Ratios')
plt.ylabel('Frequency')
plt.show()