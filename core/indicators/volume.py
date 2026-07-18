import pandas as pd
import pandas_ta_classic as ta


class VolumeIndicators:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def vwap(self):

        # Save current index
        

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