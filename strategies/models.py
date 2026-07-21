from dataclasses import dataclass, field

from core.constants.enums import Trend
from core.models.models import MarketAnalysis, OptionChainAnalysis





@dataclass(frozen=True, slots=True)
class StrategyContext:

    market: MarketAnalysis
    option_chain: OptionChainAnalysis

    # ------------------------------------------------------------------
    # Convenience Properties
    # ------------------------------------------------------------------

    @property
    def oi(self):
        return self.option_chain.oi

    @property
    def pcr(self):
        return self.option_chain.pcr

    @property
    def iv(self):
        return self.option_chain.iv

    @property
    def greeks(self):
        return self.option_chain.greeks

    @property
    def max_pain(self):
        return self.option_chain.max_pain

    # ------------------------------------------------------------------
    # Market Helpers
    # ------------------------------------------------------------------

    @property
    def bullish(self) -> bool:
        return self.market.trend == Trend.BULLISH

    @property
    def bearish(self) -> bool:
        return self.market.trend == Trend.BEARISH

    @property
    def sideways(self) -> bool:
        return self.market.trend == Trend.SIDEWAYS
    

@dataclass(frozen=True)
class MaxPainThresholds:
    MaxPainThresholds = 25
    GOOD_DISTANCE = 50
    ACCEPTABLE_DISTANCE = 100
    WEAK_DISTANCE = 150

@dataclass(frozen=True)
class GreeksThresholds:
    DELTA_STRONG = 0.60
    DELTA_MODERATE = 0.45

    GAMMA_HIGH = 0.75
    GAMMA_MEDIUM = 0.40

    THETA_LOW_DECAY = -0.10
    THETA_MEDIUM_DECAY = -0.30    

@dataclass(frozen=True)
class StrategyWeights:

    market = 35
    oi = 20
    pcr = 15
    iv = 10
    greeks = 10
    max_pain = 10


class StrategyThresholds:

    # PCR
    PCR_IDEAL_LOW = 0.8
    PCR_IDEAL_HIGH = 1.2

    # Greeks
    DELTA_STRONG = 0.60
    DELTA_MODERATE = 0.40

    # Max Pain
    MAX_PAIN_SAFE_DISTANCE = 200
    MAX_PAIN_MODERATE_DISTANCE = 100
    MAX_PAIN_LOW_DISTANCE = 50

    # IV
    IV_SPREAD_GOOD = 5
    IV_SPREAD_ACCEPTABLE = 10

