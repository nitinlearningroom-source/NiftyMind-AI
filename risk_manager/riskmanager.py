from decision_engine.enums.decision import Decision
from risk_manager.risk_assessment import RiskAssessment
from risk_manager.models.position_size import PositionSize


class RiskManager:

    def __init__(self, config, rules):

        self.config = config
        self.rules = rules

    def assess(
        self,
        context,
        account
    ) -> RiskAssessment:

        reasons = []
        warnings = []
        results = []

        approved = True

        # -----------------------------
        # Execute Risk Rules
        # -----------------------------
        for rule in self.rules:

            result = rule.evaluate(
                context=context,
                account=account,
                config=self.config
            )

            results.append(result)

            if result.reason:
                reasons.append(result.reason)

            if result.warning:
                warnings.append(result.warning)

            if not result.passed:
                approved = False

        # -----------------------------------------
        # Calculate Position Size
        # -----------------------------------------

        position_size = None

        if approved:

            risk_amount = (
                account.capital *
                self.config.risk_per_trade_pct / 100
            )
            if context.decision.decision == Decision.BUY_CALL:
                premium = context.option_chain.atm_call
            elif context.decision.decision == Decision.BUY_PUT:
                premium = context.option_chain.atm_put
            else:
                premium=0

            lot_size = context.option_chain.lot_size

            quantity = int(risk_amount / premium)

            lots = max(1, quantity // lot_size)

            quantity = lots * lot_size

            capital_required = quantity * premium

            position_size = PositionSize(

                quantity=quantity,

                lots=lots,

                capital_required=capital_required,

                max_loss=risk_amount
            )

        # -----------------------------------------
        # Return Assessment
        # -----------------------------------------

        return RiskAssessment(

            approved=approved,

            position_size=position_size,

            results=results,

            reasons=reasons,

            warnings=warnings
        )