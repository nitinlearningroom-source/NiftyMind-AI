import pandas as pd


class SupportResistanceIndicators:

    def __init__(self, df):
        self.df = df

    def pivot_points(self):

        high = self.df["High"].shift(1)
        low = self.df["Low"].shift(1)
        close = self.df["Close"].shift(1)

        pivot = (high + low + close) / 3

        self.df["PIVOT"] = pivot

        self.df["R1"] = (2 * pivot) - low
        self.df["S1"] = (2 * pivot) - high

        self.df["R2"] = pivot + (high - low)
        self.df["S2"] = pivot - (high - low)

        self.df["R3"] = high + 2 * (pivot - low)
        self.df["S3"] = low - 2 * (high - pivot)

        return self.df
    
    def donchian(self, length: int = 20):

        self.df["DONCHIAN_UPPER"] = (
            self.df["High"]
            .rolling(length)
            .max()
            .shift(1)
        )

        self.df["DONCHIAN_LOWER"] = (
            self.df["Low"]
            .rolling(length)
            .min()
            .shift(1)
        )

        self.df["DONCHIAN_MIDDLE"] = (
            self.df["DONCHIAN_UPPER"] +
            self.df["DONCHIAN_LOWER"]
        ) / 2

        return self.df