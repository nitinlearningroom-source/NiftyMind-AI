
from dataclasses import dataclass, field

@dataclass(frozen=True)
class StrategyWeights:

    market: float = 35

    oi: float = 20

    pcr: float = 15

    iv: float = 10

    greeks: float = 10

    max_pain: float = 10



@dataclass
class RuleResult:
    name: str

    passed: bool

    score: float

    weight: float

    reasons: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)
    

@dataclass(frozen=True)
class StrategyConfig:
    market_rule_pass_score: int = 28