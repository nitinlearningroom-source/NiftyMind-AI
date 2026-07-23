from brokers.dhanhq.historical_data import HistoricalDataService
from core.indicators.indicator_engine import IndicatorEngine
from data.Instrument_type import InstrumentType


history = HistoricalDataService()

df = history.get_daily("NIFTY",instrument_type= InstrumentType.INDEX,days= 250)


engine = IndicatorEngine(df)

ad= engine.calculate_all()
print(ad)

