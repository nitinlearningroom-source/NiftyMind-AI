import pandas as pd


class BaseIndicator:

    def __init__(self, df):
        self.df = df

    def _append_indicator(self, indicator_df: pd.DataFrame) -> None:
        """Append indicator columns to the existing DataFrame."""
        self.df = pd.concat([self.df, indicator_df], axis=1)