from dataclasses import dataclass, field

@dataclass(slots=True)
class RiskRuleResult:

    rule_name: str

    passed: bool

    reason: str

    warning: str | None = None