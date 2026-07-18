import pandas as pd
import pandas_ta_classic as ta

from core.indicators import base_indicator


class VolumeIndicators(base_indicator.BaseIndicator):

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def vwap(self):
        # Set Datetime as index
        self.df["Datetime"] = pd.to_datetime(self.df["Datetime"])
        self.df.set_index("Datetime", inplace=True)

        self.df["VWAP"] = ta.vwap(
            high=self.df["High"],
            low=self.df["Low"],
            close=self.df["Close"],
            volume=self.df["Volume"]
        )

        # Restore Datetime column
        self.df.reset_index(inplace=True)

        return self.df
    
    def obv(self):

        self.df["OBV"] = ta.obv(
            close=self.df["Close"],
            volume=self.df["Volume"]
        )

        return self.df