from __future__ import annotations

import pandas as pd
from core.analyzer.base_option_analyzer import BaseOptionAnalyzer
from core.constants.enums import IVTrend
from core.models.models import IVAnalysis, OptionAnalysisConfig, OptionChainSnapshot


class IVAnalyzer(BaseOptionAnalyzer):
    """
    Analyzes implied volatility across the option chain.
    """
    def __init__(self, config: OptionAnalysisConfig):
        super().__init__(config)
        
    REQUIRED_COLUMNS = [
        "strike",
        "call_iv",
        "put_iv"
    ]

    # -------------------------------------------------------------

    def analyze(
        self,
        snapshot: OptionChainSnapshot
    ) -> IVAnalysis:

        df = self.get_option_chain(snapshot)

        self.validate_columns(df, self.REQUIRED_COLUMNS)

        atm_row = self._find_atm_row(df, snapshot.spot_price)

        atm_call_iv = float(atm_row["call_iv"])
        atm_put_iv = float(atm_row["put_iv"])

        average_call_iv = self._safe_mean(df["call_iv"])
        average_put_iv = self._safe_mean(df["put_iv"])

        highest_call_iv = float(df["call_iv"].max())
        lowest_call_iv = float(df["call_iv"].min())

        highest_put_iv = float(df["put_iv"].max())
        lowest_put_iv = float(df["put_iv"].min())

        iv_skew = round(atm_put_iv - atm_call_iv, 2)

        regime = self._determine_regime(
            (atm_call_iv + atm_put_iv) / 2
        )
        iv_spread = average_put_iv-average_call_iv

        return IVAnalysis(
            atm_call_iv=round(atm_call_iv, 2),
            atm_put_iv=round(atm_put_iv, 2),

            average_call_iv=round(average_call_iv, 2),
            average_put_iv=round(average_put_iv, 2),

            highest_call_iv=round(highest_call_iv, 2),
            lowest_call_iv=round(lowest_call_iv, 2),

            highest_put_iv=round(highest_put_iv, 2),
            lowest_put_iv=round(lowest_put_iv, 2),

            iv_skew=iv_skew,
            regime=regime,
            iv_spread =iv_spread
        )

    

    # -------------------------------------------------------------

    @staticmethod
    def _find_atm_row(
        df: pd.DataFrame,
        spot_price: float
    ) -> pd.Series:

        atm_index = (df["strike"] - spot_price).abs().idxmin()

        return df.loc[atm_index]

    # -------------------------------------------------------------

    @staticmethod
    def _safe_mean(series: pd.Series) -> float:

        series = series.dropna()

        if len(series) == 0:
            return 0.0

        return float(series.mean())

    # -------------------------------------------------------------

    @staticmethod
    def _determine_regime(iv: float) -> str:

        if iv < 10:
            return "LOW"

        if iv < 20:
            return "NORMAL"

        if iv < 30:
            return "HIGH"

        return "EXTREME"
    
    def _determine_iv_trend(
        self,
        current_iv: float,
        previous_iv: float | None
    ) -> tuple[float, float, IVTrend]:

    
        if previous_iv is None:
            return (
                0.0,
                0.0,
                IVTrend.UNKNOWN
            )

        change = current_iv - previous_iv

        if previous_iv == 0:
            change_percent = 0.0
        else:
            change_percent = (change / previous_iv) * 100

        if change_percent >= 2:
            trend = IVTrend.RISING

        elif change_percent <= -2:
            trend = IVTrend.FALLING

        else:
            trend = IVTrend.STABLE

        return (
            round(change, 2),
            round(change_percent, 2),
            trend
        )