
import datetime

from core.analyzer.Underlying_Sentiments_analyzer import OptionChainAnalyzer
from core.constants.underlyings import NIFTY
from core.analyzer.Underlying_Sentiments_service import OptionChainService


analysis = OptionChainService()
option_analysis = analysis.get_option_chain(NIFTY,expiry_date="2026-07-21")

OIanalyser =OptionChainAnalyzer()
analysis = OIanalyser.analyze(snapshot=option_analysis)
print(analysis)