from Options_Rules.Rules.greeks_rule import GreeksRule
from Options_Rules.Rules.iv_rule import IVRule
from Options_Rules.Rules.market_rule import MarketRule
from Options_Rules.Rules.maxpain_rule import MaxPainRule
from Options_Rules.Rules.oi_rule import OIRule
from Options_Rules.Rules.pcr_rule import PCRRule


class RuleRegistry:

    @staticmethod
    def option_buying():

        return [

            MarketRule(),

            OIRule(),

            PCRRule(),

            GreeksRule(),

            MaxPainRule(),

            IVRule()

        ]