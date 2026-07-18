from brokers.dhanhq.market import MarketData

market = MarketData()

data = market.security_master()

print(type(data))
print(data)