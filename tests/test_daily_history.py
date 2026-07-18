from brokers.dhanhq.historical_data import HistoricalDataService

history = HistoricalDataService()

response = history.get_daily("RELIANCE", 30)

print(response)