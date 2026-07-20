from dataclasses import dataclass
from datetime import datetime
import pandas as pd
from core.models.underlying import Underlying

from core.constants.enums import (
    Breakout,
    OITrend,
    PCRTrend,
    SupportStrength,
    Trend,
    TrendStrength,
    Momentum,
    Volatility,
    Recommendation,
    VolumeConfirmation,
)
from strategies.enums import PCRSignal


@dataclass
class MarketAnalysis:
    trend: Trend
    trend_strength: TrendStrength
    momentum: Momentum
    volume_confirmation: VolumeConfirmation
    breakout: Breakout
    volatility: Volatility

    bullish_confidence: int
    bearish_confidence: int

    recommendation: Recommendation

@dataclass
class OptionAnalysisConfig :
    atm_window: int = 10
    min_oi: int = 5000
    ignore_zero_volume: bool = True
    iv_mode: str = "ATM"

@dataclass
class OptionChainAnalysis:
    """
    Aggregated analysis of the option chain.

    Produced by:
        OptionChainAnalyzer

    Contains the output of all individual analyzers.
    """

    oi_analysis: OIAnalysis
    pcr_analysis: PCRAnalysis
    iv_analysis: IVAnalysis
    max_pain_analysis: MaxPainAnalysis
    greeks_analysis: GreeksAnalysis

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
    max_call_oi_strike: str
    max_put_oi_strike: str

    trend: OITrend

@dataclass
class OptionChainSnapshot:
    underlying: Underlying
    expiry: str
    spot_price: float
    timestamp: datetime
    option_chain: pd.DataFrame

@dataclass
class PCRAnalysis:
    value: float
    signal: PCRSignal
    interpretation: str



@dataclass
class IVAnalysis:
    atm_call_iv: float
    atm_put_iv: float

    average_call_iv: float
    average_put_iv: float

    highest_call_iv: float
    lowest_call_iv: float

    highest_put_iv: float
    lowest_put_iv: float

    iv_skew: float

    iv_spread: float

    regime: str

@dataclass
class GreeksAnalysis:

    # ATM Greeks
    atm_call_delta: float
    atm_put_delta: float

    atm_call_gamma: float
    atm_put_gamma: float

    atm_call_theta: float
    atm_put_theta: float

    atm_call_vega: float
    atm_put_vega: float

    # Average Greeks
    average_call_delta: float
    average_put_delta: float

    average_call_gamma: float
    average_put_gamma: float

    average_call_theta: float
    average_put_theta: float

    average_call_vega: float
    average_put_vega: float

    # Net Greeks
    net_delta: float
    net_gamma: float
    net_theta: float
    net_vega: float
    
    interpretation: str


@dataclass
class MaxPainAnalysis:
    max_pain_strike: float
    total_loss: float

    call_loss: float
    put_loss: float

    distance_from_spot: float
    market_bias: str