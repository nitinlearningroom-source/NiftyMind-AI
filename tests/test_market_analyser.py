
from brokers.dhanhq.historical_data import HistoricalDataService
from core.analyzer.market_analyzer import MarketAnalyzer
from core.indicators.indicator_engine import IndicatorEngine


history = HistoricalDataService()

df = history.get_daily("RELIANCE", 320)


engine = IndicatorEngine(df)
engine.calculate_all()
analysis = MarketAnalyzer(engine)

print("Analysis Summary:")
print(analysis.analyze())