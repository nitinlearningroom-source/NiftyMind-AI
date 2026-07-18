from datetime import datetime, timedelta
import pandas as pd

from brokers.dhanhq.auth import DhanClient
from data.security_master import SecurityMasterManager


class HistoricalDataService:

    def __init__(self):
        self.dhan = DhanClient().get_client()
        self.security = SecurityMasterManager()

    def get_daily(self, symbol: str, days: int = 365):

        info = self.security.get_instrument_info(symbol)

        to_date = datetime.today().date()
        from_date = to_date - timedelta(days=days)

        response = self.dhan.historical_daily_data(
            security_id=info["security_id"],
            exchange_segment=info["exchange_segment"],
            instrument_type=info["instrument_type"],
            from_date=str(from_date),
            to_date=str(to_date)
        )

        return self._to_dataframe(response)

    def _to_dataframe(self, response):

        if response["status"] != "success":
            raise Exception(response["remarks"])

        data = response["data"]

        df = pd.DataFrame({
            "Datetime": pd.to_datetime(data["timestamp"], unit="s"),
            "Open": data["open"],
            "High": data["high"],
            "Low": data["low"],
            "Close": data["close"],
            "Volume": data["volume"]
        })

        df.sort_values("Datetime", inplace=True)
        df.reset_index(drop=True, inplace=True)

        return df