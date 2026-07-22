from dataclasses import dataclass, field

from decision_engine.enums.decision import Decision


@dataclass(slots=True)
class DecisionResult:

    decision: Decision

    confidence: float

    trade_allowed: bool

    reasons: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    summary: str = ""