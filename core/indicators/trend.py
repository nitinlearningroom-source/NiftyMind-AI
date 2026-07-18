import pandas as pd
import pandas_ta_classic as ta

from core.indicators import base_indicator


class TrendIndicators(base_indicator.BaseIndicator):

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def ema(self, periods):

        for period in periods:
            self.df[f"EMA_{period}"] = ta.ema(
                self.df["Close"],
                length=period
            )

        return self.df

    def supertrend(
        self,
        atr_period: int = 10,
        multiplier: float = 3.0
    ):
        """
        Calculate SuperTrend
        """

        st = ta.supertrend(
            high=self.df["High"],
            low=self.df["Low"],
            close=self.df["Close"],
            length=atr_period,
            multiplier=multiplier
        )
        st.columns = [
                "SUPERTREND",
                "SUPERTREND_DIRECTION",
                "SUPERTREND_LONG",
                "SUPERTREND_SHORT"
            ]
        self.df = pd.concat([self.df, st], axis=1)

        return self.df
    
    def adx(self, length: int = 14):

        adx = ta.adx(
            high=self.df["High"],
            low=self.df["Low"],
            close=self.df["Close"],
            length=length
        )

        print(adx.columns)   # Keep this temporarily

        adx.columns = [
            "ADX",
            "DMP",
            "DMN"
        ]

        self.df = pd.concat(
            [self.df, adx],
            axis=1
        )

        return self.df