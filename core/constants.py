from enum import Enum

class Signal(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class TrendStrength(Enum):
    SIDEWAYS = "SIDEWAYS"
    WEAK_TREND = "WEAK_TREND"
    STRONG_TREND = "STRONG_TREND"
    VERY_STRONG_TREND = "VERY_STRONG_TREND"