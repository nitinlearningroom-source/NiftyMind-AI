from brokers.dhanhq.auth import DhanClient


class MarketData:

    def __init__(self):
        self.dhan = DhanClient().get_client()

    def ticker(self, instruments):
        return self.dhan.ticker_data(instruments)

    def quote(self, instruments):
        return self.dhan.quote_data(instruments)

    def ohlc(self, instruments):
        return self.dhan.ohlc_data(instruments)

    def security_master(self):
        return self.dhan.fetch_security_list("compact")