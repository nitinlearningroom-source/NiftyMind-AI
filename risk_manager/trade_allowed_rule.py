from risk_manager.base_risk_rule import BaseRiskRule
from risk_manager.models.risk_rule_result import RiskRuleResult



class TradeAllowedRule(BaseRiskRule):

    def evaluate(
        self,
        decision,
    ):

        if not decision.trade_allowed:

            return RiskRuleResult(

                rule_name="TradeAllowedRule",

                passed=False,

                reason="",

                warning="Decision Engine rejected the trade."
            )

        return RiskRuleResult(

            rule_name="TradeAllowedRule",

            passed=True,

            reason="Trade approved by Decision Engine."
        )