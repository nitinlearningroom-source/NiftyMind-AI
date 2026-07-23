from TraderSelector.selected_trade import SelectedTrade
from decision_engine.decision_result import DecisionResult
from decision_engine.enums.decision import Decision
from option_chain.models.option_analysis import OptionAnalysis


class TradeSelector:

    def select(
        self,
        decision: DecisionResult,
        option: OptionAnalysis
    ) -> SelectedTrade:

        if decision.decision == Decision.BUY_CALL:

            return SelectedTrade(
                contract=option.atm_call,
                action="BUY"
            )

        elif decision.decision == Decision.BUY_PUT:

            return SelectedTrade(
                contract=option.atm_put,
                action="BUY"
            )

        raise ValueError("No trade selected.")