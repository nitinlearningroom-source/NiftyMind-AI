from core.constants.underlyings import NIFTY
from option_chain.option_chain_analyzer import Option_Analyzer
from option_chain.option_chain_service import Option_Service


option_service = Option_Service()

snapshot = option_service.get_option_chain(NIFTY,expiry_date="2026-07-28")

analyzer = Option_Analyzer()

analysis = analyzer.analyze(snapshot)

print(analysis.spot_price)
print(analysis.summary)
print(analysis.atm_call.ltp)

print(analysis.atm_put.ltp)
print(analysis.support)
print(analysis.resistance)
print(analysis.pcr)