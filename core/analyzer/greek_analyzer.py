from __future__ import annotations
import pandas as pd

from core.analyzer.base_option_analyzer import BaseOptionAnalyzer
from core.models.models import GreeksAnalysis, OptionAnalysisConfig, Unserlying_SentimentSnapshot



class GreeksAnalyzer(BaseOptionAnalyzer):
   

    def __init__(self, config: OptionAnalysisConfig):
        super().__init__(config)

    REQUIRED_COLUMNS = [
        "strike",

        "call_delta",
        "put_delta",

        "call_gamma",
        "put_gamma",

        "call_theta",
        "put_theta",

        "call_vega",
        "put_vega"
    ]

    # -------------------------------------------------------

    def analyze(
        self,
        snapshot: Unserlying_SentimentSnapshot
    ) -> GreeksAnalysis:

        df = self.get_option_chain(snapshot)

        self.validate_columns(df, self.REQUIRED_COLUMNS)

        atm_row = self._find_atm_row(
            df,
            snapshot.spot_price
        )

        return GreeksAnalysis(

            # ATM Greeks

            atm_call_delta=self._round(atm_row["call_delta"]),
            atm_put_delta=self._round(atm_row["put_delta"]),

            atm_call_gamma=self._round(atm_row["call_gamma"]),
            atm_put_gamma=self._round(atm_row["put_gamma"]),

            atm_call_theta=self._round(atm_row["call_theta"]),
            atm_put_theta=self._round(atm_row["put_theta"]),

            atm_call_vega=self._round(atm_row["call_vega"]),
            atm_put_vega=self._round(atm_row["put_vega"]),

            # Average Greeks

            average_call_delta=self._mean(df["call_delta"]),
            average_put_delta=self._mean(df["put_delta"]),

            average_call_gamma=self._mean(df["call_gamma"]),
            average_put_gamma=self._mean(df["put_gamma"]),

            average_call_theta=self._mean(df["call_theta"]),
            average_put_theta=self._mean(df["put_theta"]),

            average_call_vega=self._mean(df["call_vega"]),
            average_put_vega=self._mean(df["put_vega"]),

            # Net Greeks

            net_delta=self._net_delta(df),

            net_gamma=self._net_gamma(df),

            net_theta=self._net_theta(df),

            net_vega=self._net_vega(df),

            interpretation=self._interpret(df)
        )

    # -------------------------------------------------------

    @staticmethod
    def _find_atm_row(
        df: pd.DataFrame,
        spot_price: float
    ) -> pd.Series:

        atm_index = (
            df["strike"] - spot_price
        ).abs().idxmin()

        return df.loc[atm_index]

    # -------------------------------------------------------

    @staticmethod
    def _round(value) -> float:

        return round(float(value), 4)

    # -------------------------------------------------------

    def _mean(
        self,
        series: pd.Series
    ) -> float:

        return self._round(series.dropna().mean())

    # -------------------------------------------------------

    def _net_delta(
        self,
        df: pd.DataFrame
    ) -> float:

        value = (
            df["call_delta"].sum()
            +
            df["put_delta"].sum()
        )

        return self._round(value)

    # -------------------------------------------------------

    def _net_gamma(
        self,
        df: pd.DataFrame
    ) -> float:

        value = (
            df["call_gamma"].sum()
            +
            df["put_gamma"].sum()
        )

        return self._round(value)

    # -------------------------------------------------------

    def _net_theta(
        self,
        df: pd.DataFrame
    ) -> float:

        value = (
            df["call_theta"].sum()
            +
            df["put_theta"].sum()
        )

        return self._round(value)

    # -------------------------------------------------------

    def _net_vega(
        self,
        df: pd.DataFrame
    ) -> float:

        value = (
            df["call_vega"].sum()
            +
            df["put_vega"].sum()
        )

        return self._round(value)

    # -------------------------------------------------------

    def _interpret(
        self,
        df: pd.DataFrame
    ) -> str:

        delta = self._net_delta(df)

        gamma = self._net_gamma(df)

        theta = self._net_theta(df)

        vega = self._net_vega(df)

        messages = []

        if delta > 2:
            messages.append("Bullish Delta")

        elif delta < -2:
            messages.append("Bearish Delta")

        else:
            messages.append("Neutral Delta")

        if gamma > 1:
            messages.append("High Gamma")

        if theta < -5:
            messages.append("Rapid Time Decay")

        if vega > 5:
            messages.append("High Volatility Sensitivity")

        return ", ".join(messages)