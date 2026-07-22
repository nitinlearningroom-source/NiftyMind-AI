

from core.analyzer import option_chain_analyzer
from core.analyzer.market_analyzer import MarketAnalyzer
from core.constants.underlyings import NIFTY
from decision_engine.decision_engine import DecisionEngine
from services.option_chain_service import OptionChainService
from strategies.Rules.rule_engine import RuleEngine
from strategies.Rules.rule_registry import RuleRegistry
from strategies.models import StrategyContext



from brokers.dhanhq.historical_data import HistoricalDataService
from core.analyzer.market_analyzer import MarketAnalyzer
from core.indicators.indicator_engine import IndicatorEngine


history = HistoricalDataService()

df = history.get_daily("RELIANCE", 320)


indicator_engine = IndicatorEngine(df)
indicator_engine.calculate_all()

analysis = OptionChainService()
option_analysis = analysis.get_option_chain(NIFTY,expiry_date="2026-07-21")

market = MarketAnalyzer(indicator_engine).analyze()
option = option_chain_analyzer.OptionChainAnalyzer().analyze(snapshot=option_analysis)


engine: RuleEngine[list] = RuleEngine(
    RuleRegistry.option_buying()
)

context = StrategyContext(
    market=market,
    option_chain=option,
     
)
rule_result = engine.evaluate(context)
decision_engine = DecisionEngine();
decision_result = decision_engine.decide(context=market,rule_result=rule_result)
print("decision engine", decision_result)
