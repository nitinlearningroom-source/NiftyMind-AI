from enum import Enum


class Trend(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    SIDEWAYS = "SIDEWAYS"


class TrendStrength(Enum):
    WEAK = "WEAK"
    MODERATE = "MODERATE"
    STRONG = "STRONG"
    VERY_STRONG = "VERY_STRONG"


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
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"

class OITrend(Enum):
    BULLISH = "Bullish"
    BEARISH = "Bearish"
    NEUTRAL = "Neutral"


class IVLevel(Enum):
    LOW = "Low"
    NORMAL = "Normal"
    HIGH = "High"
    EXTREME = "Extreme"


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