from core.constants.enums import Recommendation
from decision_engine.decision_config import DecisionConfig
from decision_engine.decision_result import DecisionResult
from decision_engine.enums.decision import Decision


class DecisionEngine:

    def __init__(self):

        self.config = DecisionConfig()

    def decide(self, context, rule_result):

        confidence = rule_result.confidence

        reasons = []
        warnings = []

        # -----------------------------------
        # Collect Rule Results
        # -----------------------------------

        for result in rule_result.results:

            reasons.extend(result.reasons)

            warnings.extend(result.warnings)

        # -----------------------------------
        # Confidence Filter
        # -----------------------------------

        if confidence < self.config.MIN_CONFIDENCE:

            warnings.append(
                f"Confidence below {self.config.MIN_CONFIDENCE}%"
            )

            return DecisionResult(

                decision=Decision.NO_TRADE,

                confidence=confidence,

                trade_allowed=False,

                reasons=reasons,

                warnings=warnings,

                summary="Trade rejected due to low confidence."
            )

        # -----------------------------------
        # Market Recommendation
        # -----------------------------------

        recommendation = context.market.recommendation

        if recommendation == Recommendation.BUY_CALL:

            decision = Decision.BUY_CALL

            summary = "Bullish market. BUY CALL recommended."

        elif recommendation == Recommendation.BUY_PUT:

            decision = Decision.BUY_PUT

            summary = "Bearish market. BUY PUT recommended."

        else:

            decision = Decision.NO_TRADE

            summary = "No trading opportunity detected."

        # -----------------------------------
        # Final Result
        # -----------------------------------

        return DecisionResult(

            decision=decision,

            confidence=confidence,

            trade_allowed=decision != Decision.NO_TRADE,

            reasons=reasons,

            warnings=warnings,

            summary=summary
        )