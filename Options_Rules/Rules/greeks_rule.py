from Options_Rules.Rules.base_rule import BaseRule
from Options_Rules.models import StrategyContext, StrategyWeights


class GreeksRule(BaseRule):
    """
    Greeks Rule

    Evaluates:
    - Net Delta
    - Net Gamma
    - Net Theta
    - Net Vega
    - Greeks Interpretation

    Maximum Score : 10
    """

    @property
    def name(self) -> str:
        return "Greeks Rule"

    @property
    def weight(self) -> int:
        return StrategyWeights.greeks

    # ---------------------------------------------------------
    # Score
    # ---------------------------------------------------------

    def calculate_score(self, context: StrategyContext) -> int:

        greeks = context.underlying_Sentiment.greeks_analysis

        score = 0

        # -------------------------------------------------
        # Delta (4)
        # -------------------------------------------------

        if context.bullish:

            if greeks.net_delta >= 0.60:
                score += 4
            elif greeks.net_delta >= 0.40:
                score += 3
            elif greeks.net_delta >= 0.20:
                score += 2

        elif context.bearish:

            if greeks.net_delta <= -0.60:
                score += 4
            elif greeks.net_delta <= -0.40:
                score += 3
            elif greeks.net_delta <= -0.20:
                score += 2

        # -------------------------------------------------
        # Gamma (2)
        # -------------------------------------------------

        if abs(greeks.net_gamma) >= 0.05:
            score += 2

        elif abs(greeks.net_gamma) >= 0.02:
            score += 1

        # -------------------------------------------------
        # Theta (2)
        # -------------------------------------------------

        if abs(greeks.net_theta) <= 5:
            score += 2

        elif abs(greeks.net_theta) <= 10:
            score += 1

        # -------------------------------------------------
        # Vega (2)
        # -------------------------------------------------

        if greeks.net_vega >= 10:
            score += 2

        elif greeks.net_vega >= 5:
            score += 1

        return min(score, self.weight)

    # ---------------------------------------------------------
    # Reasons
    # ---------------------------------------------------------

    def build_reasons(self, context: StrategyContext) -> list[str]:

        greeks = context.underlying_Sentiment.greeks_analysis

        return [

            f"Net Delta : {greeks.net_delta:.2f}",

            f"Net Gamma : {greeks.net_gamma:.4f}",

            f"Net Theta : {greeks.net_theta:.2f}",

            f"Net Vega : {greeks.net_vega:.2f}",

            f"ATM Call Delta : {greeks.atm_call_delta:.2f}",

            f"ATM Put Delta : {greeks.atm_put_delta:.2f}",

            f"ATM Call Gamma : {greeks.atm_call_gamma:.4f}",

            f"ATM Put Gamma : {greeks.atm_put_gamma:.4f}",

            f"Interpretation : {greeks.interpretation}",

        ]

    # ---------------------------------------------------------
    # Warnings
    # ---------------------------------------------------------

    def build_warnings(self, context: StrategyContext) -> list[str]:

        greeks = context.underlying_Sentiment.greeks_analysis

        warnings = []

        # Weak Delta

        if context.bullish and greeks.net_delta < 0.20:
            warnings.append(
                "Weak bullish delta."
            )

        if context.bearish and greeks.net_delta > -0.20:
            warnings.append(
                "Weak bearish delta."
            )

        # Low Gamma

        if abs(greeks.net_gamma) < 0.02:
            warnings.append(
                "Low gamma indicates slower price movement."
            )

        # High Theta

        if abs(greeks.net_theta) > 10:
            warnings.append(
                "High theta decay may reduce option value quickly."
            )

        # Low Vega

        if greeks.net_vega < 5:
            warnings.append(
                "Low vega may limit gains from IV expansion."
            )

        return warnings