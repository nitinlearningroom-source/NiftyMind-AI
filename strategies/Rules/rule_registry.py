


from strategies.Rules.greeks_rule import GreeksRule
from strategies.Rules.iv_rule import IVRule
from strategies.Rules.market_rule import MarketRule
from strategies.Rules.maxpain_rule import MaxPainRule
from strategies.Rules.oi_rule import OIRule
from strategies.Rules.pcr_rule import PCRRule


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