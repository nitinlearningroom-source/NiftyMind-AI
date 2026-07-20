from dataclasses import dataclass

from core.analyzer.market_analysis import MarketAnalysis
from core.analyzer.option_chain_analysis import OptionChainAnalysis


@dataclass(frozen=True)
class StrategyContext:

    market: MarketAnalysis
    option_chain: OptionChainAnalysis