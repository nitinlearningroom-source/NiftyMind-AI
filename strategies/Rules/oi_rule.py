
from core.constants.enums import OITrend, Trend
from strategies.Rules.base_rule import BaseRule
from strategies.Rules.models import StrategyWeights
from strategies.models import StrategyContext


class OIRule(BaseRule):
    """
    Open Interest Rule

    Evaluates:
    - OI Trend
    - Call Writing
    - Put Writing
    - Support & Resistance
    - OI Strength

    Maximum Score : 20
    """

    @property
    def name(self) -> str:
        return "Open Interest Rule"

    @property
    def weight(self) -> int:
        return StrategyWeights.oi

    # ---------------------------------------------------------
    # Score
    # ---------------------------------------------------------

    def calculate_score(self, context: StrategyContext) -> int:

        oi = context.underlying_Sentiment.oi_analysis
        print(oi)

        score = 0

        # ----------------------------------------------
        # Trend Confirmation (8)
        # ----------------------------------------------

        if context.bullish and oi.trend == OITrend.BULLISH:
            score += 8

        elif context.bearish and oi.trend == OITrend.BEARISH:
            score += 8

        if context.bullish:
            if oi.put_writing:
                score += 4

            if oi.call_writing:
                score += 1

        elif context.bearish:
            if oi.call_writing:
                score += 4

            if oi.put_writing:
                score += 1

        # ----------------------------------------------
        # Strong Support (2)
        # ----------------------------------------------

        if oi.support_strength >= 70:
            score += 2

        elif oi.support_strength >= 50:
            score += 1

        # ----------------------------------------------
        # Strong Resistance (2)
        # ----------------------------------------------

        if oi.resistance_strength >= 70:
            score += 2

        elif oi.resistance_strength >= 50:
            score += 1

        return min(score, self.weight)

    # ---------------------------------------------------------
    # Reasons
    # ---------------------------------------------------------

    def build_reasons(self, context: StrategyContext) -> list[str]:

        oi = context.underlying_Sentiment.oi_analysis

        return [

            f"OI Trend : {oi.trend.name}",

            f"Support : {oi.support}",

            f"Resistance : {oi.resistance}",

            f"Support Strength : {oi.support_strength:.2f}%",

            f"Resistance Strength : {oi.resistance_strength:.2f}%",

            f"Put Writing : {'Yes' if oi.put_writing else 'No'}",

            f"Call Writing : {'Yes' if oi.call_writing else 'No'}",

            f"Highest Put OI : {oi.max_put_oi_strike}",

            f"Highest Call OI : {oi.max_call_oi_strike}",

            f"Total Put OI : {oi.total_put_oi:,}",

            f"Total Call OI : {oi.total_call_oi:,}",

        ]

    # ---------------------------------------------------------
    # Warnings
    # ---------------------------------------------------------

    def build_warnings(self, context: StrategyContext) -> list[str]:

        oi = context.underlying_Sentiment.oi_analysis

        warnings = []

        # Market trend mismatch

        if context.bullish and oi.trend != Trend.BULLISH:
            warnings.append(
                "OI trend does not support bullish market."
            )

        if context.bearish and oi.trend != Trend.BEARISH:
            warnings.append(
                "OI trend does not support bearish market."
            )

        # Weak support

        if oi.support_strength < 50:
            warnings.append(
                "Support strength is weak."
            )

        # Weak resistance

        if oi.resistance_strength < 50:
            warnings.append(
                "Resistance strength is weak."
            )

        # No Put Writing

        if not oi.put_writing:
            warnings.append(
                "No significant Put Writing observed."
            )

        # No Call Writing

        if not oi.call_writing:
            warnings.append(
                "No significant Call Writing observed."
            )

        return warnings