from enum import Enum


class Trend(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    SIDEWAYS = "SIDEWAYS"


class TrendStrength(Enum):
    SIDEWAYS = "SIDEWAYS"
    WEAK = "WEAK_TREND"
    STRONG = "STRONG_TREND"
    MODERATE = "MODERATE"
    VERY_STRONG = "VERY_STRONG_TREND"


class Momentum(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


class Volatility(Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"


class Recommendation(Enum):
    BUY_CALL = "BUY_CALL"
    BUY_PUT = "BUY_PUT"
    NO_TRADE = "NO_TRADE"

class Breakout(Enum):
    NONE = "NONE"
    BREAKOUT = "BREAKOUT"
    BEARISH = "BEARISH"
    BULLISH = "BULLISH"

class OITrend(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


class IVLevel(Enum):
    LOW = "LOW"
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    EXTREME = "EXTREME"


class WritingType(Enum):
    NONE = "None"
    CALL_WRITING = "Call Writing"
    PUT_WRITING = "Put Writing"


class SupportStrength(Enum):
    WEAK = "Weak"
    MODERATE = "Moderate"
    STRONG = "Strong"


class Signal(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class TrendStrength(Enum):
    SIDEWAYS = "SIDEWAYS"
    WEAK = "WEAK_TREND"
    STRONG = "STRONG_TREND"
    MODERATE="MODERATE"
    VERY_STRONG = "VERY_STRONG_TREND"


class InstrumentType(Enum):
    INDEX = "INDEX"
    STOCK = "STOCK"
    COMMODITY = "COMMODITY"
    CURRENCY = "CURRENCY"

class IVTrend(str, Enum):
    RISING = "RISING"
    FALLING = "FALLING"
    STABLE = "STABLE"
    UNKNOWN = "UNKNOWN"

class VolumeConfirmation(Enum):
    CONFIRMED = "CONFIRMED"
    NOT_CONFIRMED = "NOT_CONFIRMED"

class PCRTrend(Enum):
    BULLISH = "Bullish"
    BEARISH = "Bearish"
    NEUTRAL = "Neutral"