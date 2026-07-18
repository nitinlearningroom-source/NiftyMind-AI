from brokers.dhanhq.market import MarketData


class SecurityMasterManager:

    def __init__(self):
        self.market = MarketData()
        self.df = None
        self.symbol_index = {}

    def load(self):
        if self.df is None:
            print("Loading Security Master...")
            self.df = self.market.security_master()

            # Normalize text columns
            text_columns = [
                "SEM_TRADING_SYMBOL",
                "SEM_CUSTOM_SYMBOL",
                "SM_SYMBOL_NAME",
                "SEM_EXM_EXCH_ID",
                "SEM_SEGMENT",
                "SEM_SERIES",
            ]

            for col in text_columns:
                self.df[col] = (
                    self.df[col]
                    .fillna("")
                    .astype(str)
                    .str.strip()
                    .str.upper()
                )

            print(f"Loaded {len(self.df)} instruments.")
            equities = self.df[
                (self.df["SEM_EXM_EXCH_ID"] == "NSE")
                & (self.df["SEM_SEGMENT"] == "E")
                & (self.df["SEM_SERIES"] == "EQ")
            ]

            self.symbol_index = {
                row["SEM_TRADING_SYMBOL"]: row
                for _, row in equities.iterrows()
            }
            print(f"Indexed {len(self.symbol_index)} NSE Equity symbols.")
        return self.df  
    
    def get_security(self, symbol: str):
        self.load()
        return self.symbol_index.get(symbol.strip().upper())


    def get_security_id(self, symbol: str):
        row = self.get_security(symbol)

        if row is None:
            return None

        return int(row["SEM_SMST_SECURITY_ID"])
    def get_instrument_info(self, symbol: str):
        """
        Returns all information required by Dhan APIs.
        """

        row = self.get_security(symbol)

        if row is None:
            raise ValueError(f"Symbol '{symbol}' not found.")

        # Exchange Segment Mapping
        if row["SEM_EXM_EXCH_ID"] == "NSE" and row["SEM_SEGMENT"] == "E":
            exchange_segment = "NSE_EQ"
        elif row["SEM_EXM_EXCH_ID"] == "NSE" and row["SEM_SEGMENT"] == "D":
            exchange_segment = "NSE_FNO"
        elif row["SEM_EXM_EXCH_ID"] == "BSE":
            exchange_segment = "BSE_EQ"
        else:
            raise ValueError(
                f"Unsupported Exchange/Segment : "
                f'{row["SEM_EXM_EXCH_ID"]}-{row["SEM_SEGMENT"]}'
            )

        return {
            "symbol": row["SEM_TRADING_SYMBOL"],
            "security_id": str(int(row["SEM_SMST_SECURITY_ID"])),
            "exchange_segment": exchange_segment,
            "instrument_type": row["SEM_INSTRUMENT_NAME"],
            "series": row["SEM_SERIES"],
            "instrument_code": row["SEM_EXCH_INSTRUMENT_TYPE"]
        }