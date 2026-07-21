from brokers.dhanhq.market_data import MarketDataService

market = MarketDataService()

print(market.get_security_id("RELIANCE"))
print(market.get_security_id("TCS"))
print(market.get_security_id("INFY"))

