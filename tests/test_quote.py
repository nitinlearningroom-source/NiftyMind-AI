from brokers.dhanhq.market_data import MarketDataService

market = MarketDataService()

quote = market.get_ltp("RELIANCE")

print(quote)