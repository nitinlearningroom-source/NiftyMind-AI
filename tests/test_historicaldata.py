from brokers.dhanhq.historical_data import HistoricalDataService
from data import Instrument_type
from data.Instrument_type import InstrumentType
from data.security_master import SecurityMasterManager


history = HistoricalDataService()

#df = history.get_daily("RELIANCE",instrument_type=InstrumentType.EQUITY,days=320)

df = history.get_daily("BANKNIFTY",instrument_type=InstrumentType.INDEX,
                        days=1)

print(df)
