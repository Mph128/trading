from processing import leverage_testing as ltest
from data import historical_data
import time
lt = ltest.LeverageTesting('spy', '1d')

lt.set_time_range('2004-10-01', '2010-11-01')

print('start date: ', lt.get_start_date())
print('end date: ', lt.get_end_date())


## Testing the statistics
# print("sharpe ratio 1: " ,lt.get_leveraged_sharpe_ratio())
# print("sharpe ratio 2: " ,lt.get_unleveraged_sharpe_ratio())
# print("sortino ratio: ", lt.get_sortino_ratio())
# print("max drawdown: ", lt.get_max_drawdown())
# print("annual return: ", lt.get_annual_return())
# print("annual volatility: ", lt.get_annual_volatility())
# print("cumulative return: ", lt.get_cumulative_return())


## calculate the optimal leverage equation
lt.calculate_leverage_equation()

