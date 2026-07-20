

from core.constants.enums import Breakout, Momentum, Trend, TrendStrength, Volatility, VolumeConfirmation
from strategies.Rules.base_rule import BaseRule
from strategies.Rules.models import StrategyWeights
from strategies.models import StrategyContext


class MarketRule(BaseRule):
    """
    Evaluates the overall market condition.

    Maximum Score : 35
    """

    @property
    def name(self) -> str:
        return "Market Rule"

    @property
    def weight(self) -> int:
        return StrategyWeights.market

    # ---------------------------------------------------------
    # Score
    # ---------------------------------------------------------

    def calculate_score(self, context: StrategyContext) -> int:

        market = context.market

        score = 0

        # -------------------------------------------------
        # Trend (15)
        # -------------------------------------------------

        if market.trend == Trend.BULLISH:
            score += 15

        elif market.trend == Trend.BEARISH:
            score += 15

        # Sideways gets no directional score

        # -------------------------------------------------
        # Trend Strength (8)
        # -------------------------------------------------

        if market.trend_strength == TrendStrength.VERY_STRONG:
            score += 8

        elif market.trend_strength == TrendStrength.STRONG:
            score += 6

        elif market.trend_strength == TrendStrength.MODERATE:
            score += 4

        elif market.trend_strength == TrendStrength.WEAK:
            score += 2

        # -------------------------------------------------
        # Momentum (5)
        # -------------------------------------------------

        if context.bullish and market.momentum == Momentum.BULLISH:
            score += 5

        elif context.bearish and market.momentum == Momentum.BEARISH:
            score += 5

        elif market.momentum == Momentum.NEUTRAL:
            score += 2

        # -------------------------------------------------
        # Volume Confirmation (3)
        # -------------------------------------------------

        if market.volume_confirmation == VolumeConfirmation.CONFIRMED:
            score += 3

        # -------------------------------------------------
        # Breakout (2)
        # -------------------------------------------------

        if context.bullish and market.breakout == Breakout.BULLISH:
            score += 2

        elif context.bearish and market.breakout == Breakout.BEARISH:
            score += 2

        elif market.breakout == Breakout.BREAKOUT:
            score += 1

        # -------------------------------------------------
        # Volatility (2)
        # -------------------------------------------------

        if market.volatility == Volatility.NORMAL:
            score += 2

        elif market.volatility == Volatility.LOW:
            score += 1

        # HIGH = 0

        return min(score, self.weight)

    # ---------------------------------------------------------
    # Reasons
    # ---------------------------------------------------------

    def build_reasons(self, context: StrategyContext) -> list[str]:

        market = context.market

        return [

            f"Trend : {market.trend.name}",

            f"Trend Strength : {market.trend_strength.name}",

            f"Momentum : {market.momentum.name}",

            f"Volume : {market.volume_confirmation.name}",

            f"Breakout : {market.breakout.name}",

            f"Volatility : {market.volatility.name}",

            f"Bullish Confidence : {market.bullish_confidence}%",

            f"Bearish Confidence : {market.bearish_confidence}%",

            f"Recommendation : {market.recommendation.name}",

        ]

    # ---------------------------------------------------------
    # Warnings
    # ---------------------------------------------------------

    def build_warnings(self, context: StrategyContext) -> list[str]:

        market = context.market

        warnings = []

        # ------------------------------------------
        # Sideways Market
        # ------------------------------------------

        if market.trend == Trend.SIDEWAYS:
            warnings.append(
                "Market is moving sideways."
            )

        # ------------------------------------------
        # Weak Trend
        # ------------------------------------------

        if market.trend_strength == TrendStrength.WEAK:
            warnings.append(
                "Trend strength is weak."
            )

        elif market.trend_strength == TrendStrength.SIDEWAYS:
            warnings.append(
                "No clear market trend."
            )

        # ------------------------------------------
        # Volume
        # ------------------------------------------

        if market.volume_confirmation == VolumeConfirmation.NOT_CONFIRMED:
            warnings.append(
                "Volume does not confirm the move."
            )

        # ------------------------------------------
        # Breakout
        # ------------------------------------------

        if context.bullish and market.breakout == Breakout.BEARISH:
            warnings.append(
                "Bearish breakout against bullish trend."
            )

        if context.bearish and market.breakout == Breakout.BULLISH:
            warnings.append(
                "Bullish breakout against bearish trend."
            )

        # ------------------------------------------
        # High Volatility
        # ------------------------------------------

        if market.volatility == Volatility.HIGH:
            warnings.append(
                "High volatility. Option premiums may be expensive."
            )

        return warnings