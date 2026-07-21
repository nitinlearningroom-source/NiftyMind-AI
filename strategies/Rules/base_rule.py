from abc import ABC, abstractmethod

from strategies.Rules.models import RuleResult
from strategies.config import StrategyConfig
from strategies.models import StrategyContext


class BaseRule(ABC):
    """
    Base class for all strategy rules.

    Implements the Template Method pattern.
    """

    def __init__(self, config: StrategyConfig | None = None):
        self.config = config or StrategyConfig()

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def weight(self) -> int:
        ...

    def evaluate(self, context: StrategyContext) -> RuleResult:
        """
        Executes the rule.
        """

        score = self.calculate_score(context)

        return RuleResult(
            name=self.name,
            passed=self.is_pass(score),
            score=score,
            weight=self.weight,
            reasons=self.build_reasons(context),
            warnings=self.build_warnings(context),
        )

    def is_pass(self, score: int) -> bool:
        """
        Rule passes if it scores at least 75% of its weight.
        """
        return score >= (self.weight * 0.75)

    @abstractmethod
    def calculate_score(self, context: StrategyContext) -> int:
        ...

    @abstractmethod
    def build_reasons(self, context: StrategyContext) -> list[str]:
        ...

    def build_warnings(self, context: StrategyContext) -> list[str]:
        """
        Optional override.
        """
        return []