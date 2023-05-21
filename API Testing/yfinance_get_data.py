import yfinance as yf

msft = yf.Ticker("MSFT")

# get stock info
msft.info

# get historical market data
# (period="1mo")
# (period="max")
# interval: str = "1d"

# this is optional, default is None
# start: 'YYYY-MM-DD', end: 'YYYY-MM-DD'
period = "1mo"
interval = "1d"
hist = msft.history(period=period, interval=interval)
print(hist)

# show actions (dividends, splits)
msft.actions

# show dividends
msft.dividends

# show splits
msft.splits

# # show financials
# msft.financials
# msft.quarterly_financials

# show balance heet
msft.balance_sheet
msft.quarterly_balance_sheet

# show cashflow
msft.cashflow
msft.quarterly_cashflow

# show earnings
msft.earnings
msft.quarterly_earnings

# show sustainability
msft.sustainability

# show analysts recommendations
msft.recommendations

# show next event (earnings, etc)
msft.calendar

# show options expirations
msft.options

# get option chain for specific expiration
opt = msft.option_chain('YYYY-MM-DD')
# data available via: opt.calls, opt.puts