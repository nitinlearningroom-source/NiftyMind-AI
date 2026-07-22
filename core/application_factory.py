from risk_manager.capital_rule import CapitalRule
from risk_manager.daily_loss_rule import DailyLossRule
from risk_manager.max_position_rule import MaxPositionRule
from risk_manager.risk_config import RiskConfig
from risk_manager.riskmanager import RiskManager
from risk_manager.trade_allowed_rule import TradeAllowedRule


class ApplicationFactory:

    @staticmethod
    def create_risk_manager():

        return RiskManager(
            config=RiskConfig(),
            rules=[
                TradeAllowedRule(),
                DailyLossRule(),
                CapitalRule(),
                MaxPositionRule()
            ]
        )