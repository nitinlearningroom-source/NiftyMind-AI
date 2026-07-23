from Options_Rules.Rules.base_rule import BaseRule
from Options_Rules.models import StrategyContext, StrategyWeights
from core.constants.enums import PCRTrend

class PCRRule(BaseRule):
    """
    Put Call Ratio Rule

    Evaluates:
    - PCR Trend
    - PCR Signal
    - PCR Value

    Maximum Score : 15
    """

    @property
    def name(self) -> str:
        return "PCR Rule"

    @property
    def weight(self) -> int:
        return StrategyWeights.pcr

    # ---------------------------------------------------------
    # Score
    # ---------------------------------------------------------

    def calculate_score(self, context: StrategyContext) -> int:

        pcr = context.underlying_Sentiment.pcr_analysis

        score = 0

        # -------------------------------------------------
        # Trend Confirmation (8)
        # -------------------------------------------------

        if context.bullish and pcr.signal == PCRTrend.BULLISH:
            score += 8

        elif context.bearish and pcr.signal == PCRTrend.BEARISH:
            score += 8

        # -------------------------------------------------
        # Signal Strength (4)
        # -------------------------------------------------

        signal = pcr.signal

        if context.bullish:

            if signal == "BULLISH":
                score += 4

            elif signal == "NEUTRAL":
                score += 2

        elif context.bearish:

            if signal == "BEARISH":
                score += 4

            elif signal == "NEUTRAL":
                score += 2

        # -------------------------------------------------
        # PCR Value (3)
        # -------------------------------------------------

        if 0.8 <= pcr.value <= 1.2:
            score += 3

        elif 0.6 <= pcr.value <= 1.4:
            score += 2

        elif 0.4 <= pcr.value <= 1.6:
            score += 1

        return min(score, self.weight)

    # ---------------------------------------------------------
    # Reasons
    # ---------------------------------------------------------

    def build_reasons(self, context: StrategyContext) -> list[str]:

        pcr = pcr = context.underlying_Sentiment.pcr_analysis

        return [

            f"PCR Value : {pcr.value:.2f}",

            f"Signal : {pcr.signal}",

            f"Interpretation : {pcr.interpretation}",

        ]

    # ---------------------------------------------------------
    # Warnings
    # ---------------------------------------------------------

    def build_warnings(self, context: StrategyContext) -> list[str]:

        pcr = pcr = context.underlying_Sentiment.pcr_analysis

        warnings = []

        # Trend mismatch

        if context.bullish and pcr.signal != PCRTrend.BULLISH:
            warnings.append(
                "PCR trend does not support bullish market."
            )

        if context.bearish and pcr.signal != PCRTrend.BEARISH:
            warnings.append(
                "PCR trend does not support bearish market."
            )

        # Extreme PCR

        if pcr.value > 1.50:
            warnings.append(
                "PCR is extremely high. Possible overbought sentiment."
            )

        elif pcr.value < 0.50:
            warnings.append(
                "PCR is extremely low. Possible oversold sentiment."
            )

        return warnings