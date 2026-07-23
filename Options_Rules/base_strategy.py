from abc import ABC
from abc import abstractmethod

from .config import StrategyConfig
from .models import (
    StrategyContext,
    StrategyDecision,
)


class BaseStrategy(ABC):

    def __init__(
        self,
        config: StrategyConfig | None = None,
    ):

        self.config = config or StrategyConfig()

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @property
    @abstractmethod
    def strategy_type(self):
        ...

    @abstractmethod
    def generate_signal(
        self,
        context: StrategyContext,
    ) -> StrategyDecision:
        ...