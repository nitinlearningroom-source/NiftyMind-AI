from abc import ABC, abstractmethod

class BaseRiskRule(ABC):

    @abstractmethod
    def evaluate(
        self,
        decision,
        context,
        account,
        config
    ):
        pass