from enum import Enum


class StrategyType(str, Enum):
    INTRADAY_OPTION_BUYING = "INTRADAY_OPTION_BUYING"
    EXPIRY_BUYING = "EXPIRY_BUYING"
    OPTION_SELLING = "OPTION_SELLING"
    SWING = "SWING"
    BTST = "BTST"


class Signal(str, Enum):
    BUY_CALL = "BUY_CALL"
    BUY_PUT = "BUY_PUT"
    NO_TRADE = "NO_TRADE"


class ConfidenceLevel(str, Enum):
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


class TradeDirection(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    SIDEWAYS = "SIDEWAYS"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"