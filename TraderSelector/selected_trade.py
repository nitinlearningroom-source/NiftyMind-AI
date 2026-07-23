from dataclasses import dataclass

from decision_engine.decision_result import DecisionResult
from decision_engine.enums.decision import Decision
from option_chain.models.option_analysis import OptionAnalysis
from option_chain.models.option_contract import OptionContract


@dataclass(slots=True)
class SelectedTrade:

    contract: OptionContract

    action: str          # BUY / SELL

    quantity: int = 0

    lots: int = 0


class TradeSelector:

    def select(
        self,
        decision: DecisionResult,
        option: OptionAnalysis
    ) -> SelectedTrade:

        if decision.decision == Decision.BUY_CALL:

            return SelectedTrade(
                contract =option.atm_call,
                action="BUY"
            )

        elif decision.decision == Decision.BUY_PUT:

            return SelectedTrade(
                contract=option.atm_put,
                action="BUY"
            )
        elif decision.decision == Decision.NO_TRADE:
            return SelectedTrade(
                contract=option.atm_call,
                action="NO Trade"
            )
            

        raise ValueError("No trade selected.")