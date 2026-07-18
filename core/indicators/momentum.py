import pandas as pd
import pandas_ta_classic as ta


class MomentumIndicators:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def rsi(self, length=14):
        self.df["RSI"] = ta.rsi(
            self.df["Close"],
            length=length
        )
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

        print(stoch.columns)
        print(stoch.tail())

        stoch.columns = [
            "STOCH_RSI_K",
            "STOCH_RSI_D"
        ]

        self.df = pd.concat([self.df, stoch], axis=1)

        return self.df