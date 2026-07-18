from brokers.dhanhq.auth import DhanClient
from data.security_master import SecurityMasterManager


class MarketDataService:

    def __init__(self):
        self.dhan = DhanClient().get_client()
        self.security = SecurityMasterManager()

    def get_security_id(self, symbol):
        return self.security.get_security_id(symbol)

    def get_quote(self, symbol):
        security_id = self.get_security_id(symbol)

        if security_id is None:
            raise ValueError(f"{symbol} not found.")

        securities = {
            "NSE_EQ": [security_id]
        }

        return self.dhan.quote_data(securities)

    def get_ltp(self, symbol):
        quote = self.get_quote(symbol)
        return quote