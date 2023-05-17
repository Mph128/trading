from alpaca.trading.client import TradingClient
from alpaca.data.live import StockDataStream
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockLatestQuoteRequest



#saved keys
api_key = "CK1OWW6XRS8FH9DAMGAC"
secret_key = "aPG8CvIY6qOw0bfoqkxvY2dU7VPWgkvlI7lQXpEF"


# # paper=True enables paper trading
# trading_client = TradingClient(api_key, secret_key, paper=True)

# account = trading_client.get_account()

# trading_client.get_all_positions()


# keys required for stock historical data client
client = StockHistoricalDataClient(api_key, secret_key)

# multi symbol request - single symbol is similar
multisymbol_request_params = StockLatestQuoteRequest(symbol_or_symbols=["SPY", "GLD", "TLT"])

latest_multisymbol_quotes = client.get_stock_latest_quote(multisymbol_request_params)

gld_latest_ask_price = latest_multisymbol_quotes["GLD"].ask_price
print("GLD latest ask price: " + str(gld_latest_ask_price))


# wss_client = StockDataStream('api-key', 'secret-key')

# # async handler
# async def quote_data_handler(data):
#     # quote data will arrive here
#     print(data)

# wss_client.subscribe_quotes(quote_data_handler, "SPY")

# wss_client.run()