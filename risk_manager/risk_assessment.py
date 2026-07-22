from dataclasses import dataclass, field

from risk_manager.models.position_size import PositionSize
from risk_manager.models.risk_rule_result import RiskRuleResult

@dataclass(slots=True)
class RiskAssessment:

    approved: bool

    position_size: PositionSize | None

    results: list[RiskRuleResult] = field(default_factory=list)

    reasons: list[str] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)