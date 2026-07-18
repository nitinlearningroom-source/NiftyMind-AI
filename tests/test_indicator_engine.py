from brokers.dhanhq.historical_data import HistoricalDataService
from core.indicators.indicator_engine import IndicatorEngine


history = HistoricalDataService()

df = history.get_daily("RELIANCE", 250)

engine = IndicatorEngine(df)
engine.supertrend()
engine.ema()
engine.rsi()
engine.macd()
engine.atr()
engine.vwap()
engine.adx()
engine.stoch_rsi()
print(engine.summary())
