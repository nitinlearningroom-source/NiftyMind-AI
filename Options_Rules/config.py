from dataclasses import dataclass


@dataclass(frozen=True)
class StrategyConfig:

    minimum_market_confidence: float = 75.0

    minimum_strategy_score: float = 70.0

    minimum_risk_reward: float = 2.0

    minimum_pcr_bullish: float = 1.0

    maximum_iv: float = 25.0

    minimum_iv: float = 8.0

    max_distance_from_max_pain: int = 100

    allow_sideways: bool = False

    max_trade_time_minutes: int = 300