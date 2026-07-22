from risk_manager.base_risk_rule import BaseRiskRule
from risk_manager.models.risk_rule_result import RiskRuleResult


class CapitalRule(BaseRiskRule):

    def evaluate(
        self,
        decision,
        context,
        account,
        config
    ):

        premium = context.option_chain.atm_option_price

        lot_size = context.option_chain.lot_size

        required_margin = premium * lot_size

        if account.available_margin < required_margin:

            return RiskRuleResult(

                rule_name="CapitalRule",

                passed=False,

                reason="",

                warning="Insufficient available margin."
            )

        return RiskRuleResult(

            rule_name="CapitalRule",

            passed=True,

            reason="Sufficient margin available."
        )