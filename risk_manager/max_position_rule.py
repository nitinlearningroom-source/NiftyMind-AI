from risk_manager.base_risk_rule import BaseRiskRule
from risk_manager.models.risk_rule_result import RiskRuleResult


class MaxPositionRule(BaseRiskRule):

    def evaluate(
        self,
        account,
        config
    ):

        if account.open_positions >= config.max_open_positions:

            return RiskRuleResult(

                rule_name="MaxPositionRule",

                passed=False,

                reason="",

                warning="Maximum open positions reached."
            )

        return RiskRuleResult(

            rule_name="MaxPositionRule",

            passed=True,

            reason="Position limit available."
        )