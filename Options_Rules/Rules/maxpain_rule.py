
from Options_Rules.Rules.base_rule import BaseRule
from Options_Rules.models import StrategyContext, StrategyThresholds, StrategyWeights


class MaxPainRule(BaseRule):
    """
    Max Pain Rule

    Evaluates:
    - Market Bias
    - Distance from Max Pain
    - Call/Put Loss Distribution

    Maximum Score : 10
    """

    @property
    def name(self) -> str:
        return "Max Pain Rule"

    @property
    def weight(self) -> int:
        return StrategyWeights.max_pain

    # ---------------------------------------------------------
    # Score
    # ---------------------------------------------------------

    def calculate_score(self, context: StrategyContext) -> int:

        mp =  context.underlying_Sentiment.max_pain_analysis

        score = 0

        # -------------------------------------------------
        # Market Bias (5)
        # -------------------------------------------------

        bias = mp.market_bias.upper()

        if context.bullish:

            if bias == "BULLISH":
                score += 5

            elif bias == "NEUTRAL":
                score += 3

        elif context.bearish:

            if bias == "BEARISH":
                score += 5

            elif bias == "NEUTRAL":
                score += 3

        # -------------------------------------------------
        # Distance from Max Pain (3)
        # -------------------------------------------------

        distance = abs(mp.distance_from_spot)

        if distance >= StrategyThresholds.MAX_PAIN_SAFE_DISTANCE :
            score += 3

        elif distance >= StrategyThresholds.MAX_PAIN_MODERATE_DISTANCE:
            score += 2

        elif distance >= StrategyThresholds.MAX_PAIN_LOW_DISTANCE:
            score += 1

        # -------------------------------------------------
        # Loss Distribution (2)
        # -------------------------------------------------

        if context.bullish:

            if mp.call_loss > mp.put_loss:
                score += 2

        elif context.bearish:

            if mp.put_loss > mp.call_loss:
                score += 2

        return min(score, self.weight)

    # ---------------------------------------------------------
    # Reasons
    # ---------------------------------------------------------

    def build_reasons(self, context: StrategyContext) -> list[str]:

        mp =  context.underlying_Sentiment.max_pain_analysis

        return [

            f"Max Pain Strike : {mp.max_pain_strike}",

            f"Distance from Spot : {mp.distance_from_spot:.2f}",

            f"Market Bias : {mp.market_bias}",

            f"Call Loss : {mp.call_loss:,.0f}",

            f"Put Loss : {mp.put_loss:,.0f}",

            f"Total Loss : {mp.total_loss:,.0f}",

        ]

    # ---------------------------------------------------------
    # Warnings
    # ---------------------------------------------------------

    def build_warnings(self, context: StrategyContext) -> list[str]:

        mp =  context.underlying_Sentiment.max_pain_analysis

        warnings = []

        # Very close to Max Pain

        if abs(mp.distance_from_spot) < 50:
            warnings.append(
                "Spot price is very close to Max Pain."
            )

        # Market bias mismatch

        if context.bullish and mp.market_bias.upper() == "BEARISH":
            warnings.append(
                "Max Pain bias is bearish."
            )

        if context.bearish and mp.market_bias.upper() == "BULLISH":
            warnings.append(
                "Max Pain bias is bullish."
            )

        # Balanced losses

        if abs(mp.call_loss - mp.put_loss) < (0.05 * mp.total_loss):
            warnings.append(
                "Call and Put losses are nearly balanced."
            )

        return warnings