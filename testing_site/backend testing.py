from processing import leverage_testing as ltest
from data import historical_data
import time
lt = ltest.LeverageTesting('spy', '1d')
print(lt.get_close_prices())
lt.set_time_range('1994-10-01', '2023-12-31')
# print(lt.get_close_prices())
# Start the timer
# start_time = time.time()
# lt.calculate_leverage_equation()
# # End the timer
# end_time = time.time()

# Calculate the elapsed time
# elapsed_time = end_time - start_time

print (lt.leveraged_cumulative_returns)

# # Print the elapsed time
# print("Elapsed time:", elapsed_time, "seconds")