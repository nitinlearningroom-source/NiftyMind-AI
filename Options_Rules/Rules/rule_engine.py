from dataclasses import dataclass, field

from Options_Rules.Rules.models import RuleResult

@dataclass(slots=True)
class RuleEngineResult:
    total_score: int
    max_score: int

    results: list[RuleResult] = field(default_factory=list)

    @property
    def confidence(self) -> float:
        if self.max_score == 0:
            return 0.0
        return round((self.total_score / self.max_score) * 100, 2)

    @property
    def passed(self) -> bool:
        return self.confidence >= 70    
    

class RuleEngine:

    def __init__(self, rules):
        self.rules = rules

    def evaluate(self, context) -> RuleEngineResult:

        results = []

        total_score = 0

        max_score = 0

        for rule in self.rules:

            result = rule.evaluate(context)

            results.append(result)

            total_score += result.score

            max_score += result.weight

        return RuleEngineResult(
            total_score=total_score,
            max_score=max_score,
            results=results,
        )