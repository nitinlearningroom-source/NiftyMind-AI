import pandas as pd
import pandas_ta_classic as ta


class VolatilityIndicators:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def atr(self, period: int = 14):
        """
        Calculate Average True Range (ATR).
        """

        self.df[f"ATR_{period}"] = ta.atr(
            high=self.df["High"],
            low=self.df["Low"],
            close=self.df["Close"],
            length=period,
        )

        return self.df

    def bollinger(self, period: int = 20, std: float = 2.0):
        """
        Calculate Bollinger Bands.
        """

        bb = ta.bbands(
            self.df["Close"],
            length=period,
            std=std,
        )

        self.df = pd.concat([self.df, bb], axis=1)

        return self.df