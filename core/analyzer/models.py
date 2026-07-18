from dataclasses import dataclass

from core.analyzer.enums import (
    Breakout,
    Trend,
    TrendStrength,
    Momentum,
    Volatility,
    Recommendation,
)


@dataclass
class MarketAnalysis:
    trend: Trend
    trend_strength: TrendStrength
    momentum: Momentum
    volume_confirmation: bool
    breakout: Breakout
    volatility: Volatility

    bullish_confidence: int
    bearish_confidence: int

    recommendation: Recommendation