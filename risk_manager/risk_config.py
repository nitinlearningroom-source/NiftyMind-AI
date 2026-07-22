from dataclasses import dataclass

@dataclass(slots=True)
class RiskConfig:

    risk_per_trade_pct: float = 1.0

    max_daily_loss_pct: float = 3.0

    max_open_positions: int = 3

    max_capital_utilization_pct: float = 80.0