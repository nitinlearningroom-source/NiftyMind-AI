import pandas as pd
from brokers.dhanhq.market import MarketData
from data.model import Instrument

class SecurityMasterManager:

    def __init__(self):

        self.market = MarketData()
        
        self.loaded = False

        self.df = None

        self.all = {}

        self.equities = {}

        self.indices = {}

        self.futures = {}

        self.options = {}

        self.etfs = {}

        self.currency = {}

        self.commodity = {}
        

    def load(self):

        if self.loaded:
            return

        self.df  = self.market.security_master()

        self._build_indexes()

        self.loaded = True

    def _build_indexes(self):

        for _, row in self.df.iterrows():

            instrument = self._create_instrument(row)

            symbol = instrument.symbol.upper()

            self.all[symbol] = instrument

            match instrument.instrument_type:

                case "EQUITY":
                    self.equities[symbol] = instrument

                case "INDEX":
                    self.indices[symbol] = instrument

                case "FUTURE":
                    self.futures[symbol] = instrument

                case "OPTION":
                    self.options[symbol] = instrument

                case "ETF":
                    self.etfs[symbol] = instrument

                case "CURRENCY":
                    self.currency[symbol] = instrument

                case "COMMODITY":
                    self.commodity[symbol] = instrument


    def get_security(self, symbol) -> Instrument:

        self.load()

        return self.all.get(symbol.upper())
        
    def get_equity(self, symbol)-> Instrument:

        self.load()

        return self.equities.get(symbol.upper())
        
    def get_index(self, symbol)-> Instrument:

        self.load()

        return self.indices.get(symbol.upper())
        
    def get_future(self, symbol)-> Instrument:

        self.load()

        return self.futures.get(symbol.upper())
        
    def get_option(self, symbol)-> Instrument:

        self.load()

        return self.options.get(symbol.upper())
        
    def search(self, text)-> Instrument:

        self.load()

        text = text.upper()

        return [
            instrument
            for symbol, instrument in self.all.items()
                if text in symbol
        ]
    
    def _create_instrument(self, row) -> Instrument:

        return Instrument(

            security_id=str(row["SEM_SMST_SECURITY_ID"]),
            symbol=str(row["SEM_TRADING_SYMBOL"]).strip().upper(),
            exchange_segment=str(row["SEM_EXM_EXCH_ID"]),
            instrument_type=str(row["SEM_INSTRUMENT_NAME"]),

            exchange=row.get("SEM_EXM_EXCH_ID"),
            series=row.get("SEM_SERIES"),
            lot_size=int(row.get("SEM_LOT_UNITS", 1)),

            strike_price=row.get("SEM_STRIKE_PRICE"),
            expiry_date=row.get("SEM_EXPIRY_DATE"),
            option_type=row.get("SEM_OPTION_TYPE")
        )