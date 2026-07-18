import pandas as pd
import pandas_ta_classic as ta

from core.indicators import base_indicator


class MomentumIndicators(base_indicator.BaseIndicator):

    def rsi(self, length=14):
        self.df["RSI"] = ta.rsi(
            self.df["Close"],
            length=length
        )
        self.logger.info("Calculating RSI for period: %s", length)    
        return self.df

    def stoch_rsi(
        self,
        length=14,
        rsi_length=14,
        k=3,
        d=3
    ):
        stoch = ta.stochrsi(
            close=self.df["Close"],
            length=length,
            rsi_length=rsi_length,
            k=k,
            d=d
        )

        stoch.columns = [
            "STOCH_RSI_K",
            "STOCH_RSI_D"
        ]

        self.df = pd.concat([self.df, stoch], axis=1)
        self.logger.info(
            "Calculating Stochastic RSI with length: %s, rsi_length: %s, k: %s, d: %s",
            length, rsi_length, k, d
        )
        return self.df