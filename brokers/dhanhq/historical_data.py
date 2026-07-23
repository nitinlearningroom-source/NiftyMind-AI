from datetime import datetime, timedelta
import pandas as pd
from brokers.dhanhq.auth import DhanClient
from data.Instrument_type import InstrumentType
from data.model import Instrument
from data.security_master import SecurityMasterManager

class HistoricalDataService:

    def __init__(self):
        self.dhan = DhanClient().get_client()
        self.security = SecurityMasterManager()
        self.info = Instrument

    def get_daily(self, symbol: str, instrument_type: InstrumentType= InstrumentType.EQUITY, days: int = 365):
        
        
        if instrument_type == InstrumentType.EQUITY:
            self.info = self.security.get_equity(symbol)

        elif instrument_type == InstrumentType.INDEX:
            self.info = self.security.get_index(symbol)

        elif instrument_type == InstrumentType.FUTURE:
            self.info = self.security.get_future(symbol)

        elif instrument_type == InstrumentType.OPTION:
            self.info = self.security.get_option(symbol)
        else:
            raise ValueError("Unsupported instrument type")
            

        to_date = datetime.today().date()
        from_date = to_date - timedelta(days=days)

        from_date = from_date.strftime("%Y-%m-%d")
        to_date = to_date.strftime("%Y-%m-%d")

        #Define Parameters for Reliance Industries Ltd
        security_id = self.info.security_id          # Dhan Security ID for RELIANCE (NSE EQ)
        exchange_segment = self.info.exchange_segment # Equity Segment
        instrument_type1 = self.info.instrument_type   # Asset Type
        expiry_code = 0               # 0 for Equity Spot

        # Exchange Segment Mapping
        if self.info.exchange_segment.upper() == "NSE" and instrument_type == InstrumentType.EQUITY:
            exchange_segment = "NSE_EQ"
        elif self.info.exchange_segment.upper() == "NSE" and instrument_type== InstrumentType.FUTURE:
            exchange_segment = "NSE_FNO"
        elif self.info.exchange_segment.upper() == "NSE" and instrument_type== InstrumentType.INDEX:        
            exchange_segment = "IDX_I"
        elif self.info.exchange_segment.upper() == "BSE" and instrument_type == InstrumentType.EQUITY:
            exchange_segment = "BSE_EQ"
        elif self.info.exchange_segment.upper() == "BSE" and instrument_type == InstrumentType.INDEX:
            exchange_segment = "IDX_I"
        else:
            raise ValueError(
            f"Unsupported Exchange/Segment : " )

        # Fetch Data
        response = self.dhan.historical_daily_data(
            security_id=security_id,
            exchange_segment=exchange_segment,
            instrument_type=instrument_type1,
            expiry_code=expiry_code,
            from_date=from_date,
            to_date=to_date
        )
        return self._to_dataframe(response)

    def _to_dataframe(self, response) -> pd.DataFrame:
        """
        Convert Dhan historical API response into a standard OHLCV DataFrame.
        """
        if not response:
            raise ValueError("Empty response received from Dhan API.")

        if response.get("status") != "success":
            raise RuntimeError(response.get("remarks", "Unknown error from Dhan API."))

        data = response.get("data")

        if not data:
            raise ValueError("No historical data returned.")

        df = pd.DataFrame({
            "Datetime": pd.to_datetime(data["timestamp"], unit="s"),
            "Open": data["open"],
            "High": data["high"],
            "Low": data["low"],
            "Close": data["close"],
            "Volume": data["volume"],
        })

        df.sort_values("Datetime", inplace=True)
        df.reset_index(drop=True, inplace=True)

        # Future indicators expect numeric values
        numeric_cols = ["Open", "High", "Low", "Close", "Volume"]
        df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

        return df