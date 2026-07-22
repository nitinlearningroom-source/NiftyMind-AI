from risk_manager.base_risk_rule import BaseRiskRule
from risk_manager.models.risk_rule_result import RiskRuleResult


class DailyLossRule(BaseRiskRule):

    def evaluate(
        self,
        decision,
        context,
        account,
        config
    ):

        max_daily_loss = (
            account.capital *
            config.max_daily_loss_pct / 100
        )

        if account.todays_loss >= max_daily_loss:

            return RiskRuleResult(

                rule_name="DailyLossRule",

                passed=False,

                reason="",

                warning="Maximum daily loss reached."
            )

        return RiskRuleResult(

            rule_name="DailyLossRule",

            passed=True,

            reason="Daily loss within limit."
        )