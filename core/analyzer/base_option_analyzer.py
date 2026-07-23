from __future__ import annotations

from abc import ABC
import pandas as pd
from core.models.models import OptionAnalysisConfig, Unserlying_SentimentSnapshot


class BaseOptionAnalyzer(ABC):
    """
    Base class for all Option Chain analyzers.

    Provides common helper methods for:
        • Option chain filtering
        • DataFrame validation
        • ATM strike detection
    """

    def __init__(self,  config: OptionAnalysisConfig ):
        self.config=config

    # ------------------------------------------------------------

    def get_option_chain(
        self,
        snapshot: Unserlying_SentimentSnapshot
        ) -> pd.DataFrame:
        """
        Returns option chain filtered around ATM.
        """

        df = snapshot.sentiment.copy()

        if self.config.atm_window <= 0:
            return df

        return self.filter_atm_window(df, snapshot.spot_price)

    # ------------------------------------------------------------

    def filter_atm_window(
        self,
        df: pd.DataFrame,
        spot_price: float
        ) -> pd.DataFrame:

        df = df.sort_values("strike").reset_index(drop=True)

        atm_index = (df["strike"] - spot_price).abs().idxmin()

        start = max(0, atm_index - self.config.atm_window)

        end = min(len(df), atm_index + self.config.atm_window + 1)

        return df.iloc[start:end].reset_index(drop=True)

    # ------------------------------------------------------------

    @staticmethod
    def validate_columns(
        df: pd.DataFrame,
        columns: list[str]
        ):

        missing = set(columns) - set(df.columns)

        if missing:
            raise ValueError(
                f"Missing required columns : {sorted(missing)}"
            )