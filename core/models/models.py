from dataclasses import dataclass
from datetime import datetime
import pandas as pd
from core.models.underlying import Underlying

from core.constants.enums import (
    Breakout,
    IVLevel,
    OITrend,
    SupportStrength,
    Trend,
    TrendStrength,
    Momentum,
    Volatility,
    Recommendation,
    WritingType,
    InstrumentType
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

@dataclass
class OptionChainAnalysis:

    spot_price: float
    support: float
    resistance: float
    support_strength: SupportStrength
    pcr: float
    max_pain: float
    oi_trend: OITrend
    writing_type: WritingType
    iv_level: IVLevel
    bullish_confidence: int
    bearish_confidence: int

@dataclass
class OIAnalysis:
    total_call_oi: int
    total_put_oi: int

    total_call_change_oi: int
    total_put_change_oi: int

    support: int
    resistance: int

    support_strength: SupportStrength
    resistance_strength: SupportStrength

    call_writing: bool
    put_writing: bool

    trend: OITrend

@dataclass
class OptionChainSnapshot:
    underlying: Underlying
    expiry: str
    spot_price: float
    timestamp: datetime
    option_chain: pd.DataFrame