import pandas as pd
import pandas_ta_classic as ta

from core.indicators import base_indicator


class VolatilityIndicators(base_indicator.BaseIndicator):

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
        self.logger.info("Calculating ATR for period: %s", period)
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
        self.logger.info("Calculating Bollinger Bands for period: %s, std: %s", period, std)
        return self.df