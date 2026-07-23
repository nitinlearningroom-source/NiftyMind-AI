

from Options_Rules.Rules.rule_engine import RuleEngine
from Options_Rules.Rules.rule_registry import RuleRegistry
from Options_Rules.models import StrategyContext
from TraderSelector.selected_trade import TradeSelector
from brokers.dhanhq.historical_data import HistoricalDataService
from core.analyzer import Underlying_Sentiments_analyzer
from core.analyzer.Underlying_Sentiments_service import Underlying_Sentiments_Service
from core.analyzer.market_analyzer import MarketAnalyzer
from core.constants.underlyings import NIFTY
from core.indicators.indicator_engine import IndicatorEngine
from data.Instrument_type import InstrumentType
from decision_engine.decision_engine import DecisionEngine
from risk_manager.capital_rule import CapitalRule
from risk_manager.daily_loss_rule import DailyLossRule
from risk_manager.max_position_rule import MaxPositionRule
from risk_manager.risk_config import RiskConfig
from risk_manager.riskmanager import RiskManager
from risk_manager.trade_allowed_rule import TradeAllowedRule
from risk_manager.trading_account import TradingAccount



history = HistoricalDataService()


df = history.get_daily("NIFTY",InstrumentType.INDEX, 320)

indicator_engine = IndicatorEngine(df)
indicator_engine.calculate_all()
market_result = MarketAnalyzer(indicator_engine).analyze()

underlying_Sentiments_Service = Underlying_Sentiments_Service()
sentiment_analysis = underlying_Sentiments_Service.Get_Sentiment_OptionData(NIFTY,expiry_date="2026-07-28")

sentiment_result = Underlying_Sentiments_analyzer.Underlying_SentimentsAnalyzer().analyze(snapshot=sentiment_analysis)


engine: RuleEngine[list] = RuleEngine(
     RuleRegistry.option_buying()
 )

strategy_context = StrategyContext(
    market=market_result,
    underlying_Sentiment=sentiment_result,
    option_Chain=sentiment_result.Option_Analysis
 )
rule_engine_result = engine.evaluate(strategy_context)

decision_engine = DecisionEngine();
decision_result = decision_engine.decide(context=strategy_context,rule_result=rule_engine_result)

#print("decision -",decision_result);

tradeSelector = TradeSelector()
selected_trade = tradeSelector.select(decision=decision_result,option=sentiment_result.Option_Analysis)

strategy_context = StrategyContext(
    market=market_result,
    underlying_Sentiment=sentiment_result,
    option_Chain=sentiment_result.Option_Analysis,
    decision =  decision_result,
    selected_trade=selected_trade
 )


account = TradingAccount(
    capital=500000,
    available_margin=400000,
    used_margin=100000,
    todays_loss=2000,
    open_positions=1,
    max_open_positions=3
)

risk_manager = RiskManager(
    config=RiskConfig(),
    rules=[
        TradeAllowedRule(),
        DailyLossRule(),
        CapitalRule(),
        MaxPositionRule()
    ]
)

assessment = risk_manager.assess(context=strategy_context,account=account)

print("=" * 60)
print("RISK MANAGER RESULT")
print("=" * 60)

print(f"Approved : {assessment.approved}")

if assessment.position_size:
    print(f"Quantity : {assessment.position_size.quantity}")
    print(f"Lots : {assessment.position_size.lots}")
    print(f"Capital Required : {assessment.position_size.capital_required}")
    print(f"Max Loss : {assessment.position_size.max_loss}")

print("\nReasons")
for reason in assessment.reasons:
    print(f"✔ {reason}")

print("\nWarnings")
for warning in assessment.warnings:
    print(f"⚠ {warning}")
