from dataclasses import dataclass


@dataclass(slots=True)
class RiskRuleResult:

    rule_name: str

    passed: bool

    reason: str = ""

    warning: str = ""