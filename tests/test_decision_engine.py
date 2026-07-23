from core.analyzer import Underlying_Sentiments_analyzer
from core.analyzer.Underlying_Sentiments_service import Underlying_Sentiments_Service
from core.analyzer.market_analyzer import MarketAnalyzer
from core.constants.underlyings import NIFTY
from data.Instrument_type import InstrumentType
from brokers.dhanhq.historical_data import HistoricalDataService
from core.indicators.indicator_engine import IndicatorEngine
from decision_engine.decision_engine import DecisionEngine
from strategies.Rules.rule_engine import RuleEngine
from strategies.Rules.rule_registry import RuleRegistry
from strategies.models import StrategyContext


history = HistoricalDataService()
df = history.get_daily("NIFTY",instrument_type=InstrumentType.INDEX,days= 250)

print("DF",df)
indicator_engine = IndicatorEngine(df)
indicator_result=indicator_engine.calculate_all()

analysis = Underlying_Sentiments_Service()
sentiments_Service = analysis.get_option_chain(NIFTY,expiry_date="2026-07-28")

market = MarketAnalyzer(indicator_engine= indicator_engine).analyze()
underlying_Sentiment = Underlying_Sentiments_analyzer.Underlying_SentimentsAnalyzer().analyze(snapshot=sentiments_Service)


engine: RuleEngine[list] = RuleEngine(
    RuleRegistry.option_buying()
)

context = StrategyContext(
    market=market,
    underlying_Sentiment=underlying_Sentiment,
    option_Chain= None
     
)
rule_result = engine.evaluate(context)
decision_engine = DecisionEngine();
decision_result = decision_engine.decide(context=market,rule_result=rule_result)
print("decision engine", decision_result)
