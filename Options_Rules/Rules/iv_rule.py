

from Options_Rules.Rules.base_rule import BaseRule
from Options_Rules.enums import IVRegime
from Options_Rules.models import StrategyContext, StrategyWeights


class IVRule(BaseRule):
    """
    Implied Volatility Rule

    Evaluates:
    - IV Regime
    - ATM IV
    - IV Skew
    - IV Spread

    Maximum Score : 10
    """

    @property
    def name(self) -> str:
        return "IV Rule"

    @property
    def weight(self) -> int:
        return StrategyWeights.iv

    # ---------------------------------------------------------
    # Score
    # ---------------------------------------------------------

    def calculate_score(self, context: StrategyContext) -> int:

        iv = context.underlying_Sentiment.iv_analysis

        score = 0

        # -------------------------------------------------
        # IV Regime (5)
        # -------------------------------------------------

        regime = iv.regime.upper()

        if regime == IVRegime.NORMAL:
            score += 5

        elif regime == IVRegime.LOW:
            score += 4

        elif regime == IVRegime.HIGH:
            score += 2

        elif regime ==  IVRegime.EXTREME:
            score += 0

        # -------------------------------------------------
        # ATM IV Balance (2)
        # -------------------------------------------------

        diff = abs(iv.atm_call_iv - iv.atm_put_iv)

        if diff <= 2:
            score += 2

        elif diff <= 5:
            score += 1

        # -------------------------------------------------
        # IV Spread (2)
        # -------------------------------------------------

        if iv.iv_spread <= 5:
            score += 2

        elif iv.iv_spread <= 10:
            score += 1

        # -------------------------------------------------
        # IV Skew (1)
        # -------------------------------------------------

        if abs(iv.iv_skew) <= 5:
            score += 1

        return min(score, self.weight)

    # ---------------------------------------------------------
    # Reasons
    # ---------------------------------------------------------

    def build_reasons(self, context: StrategyContext) -> list[str]:

        iv = context.underlying_Sentiment.iv_analysis

        return [

            f"IV Regime : {iv.regime}",

            f"ATM Call IV : {iv.atm_call_iv:.2f}",

            f"ATM Put IV : {iv.atm_put_iv:.2f}",

            f"Average Call IV : {iv.average_call_iv:.2f}",

            f"Average Put IV : {iv.average_put_iv:.2f}",

            f"IV Spread : {iv.iv_spread:.2f}",

            f"IV Skew : {iv.iv_skew:.2f}",

        ]

    # ---------------------------------------------------------
    # Warnings
    # ---------------------------------------------------------

    def build_warnings(self, context: StrategyContext) -> list[str]:

        iv = context.underlying_Sentiment.iv_analysis

        warnings = []

        if iv.regime.upper() == "EXTREME":
            warnings.append(
                "Extreme IV detected. Premiums may be expensive."
            )

        elif iv.regime.upper() == "HIGH":
            warnings.append(
                "High IV may increase option premiums."
            )

        if iv.iv_spread > 10:
            warnings.append(
                "Large IV spread detected."
            )

        if abs(iv.iv_skew) > 10:
            warnings.append(
                "Significant IV skew detected."
            )

        return warnings