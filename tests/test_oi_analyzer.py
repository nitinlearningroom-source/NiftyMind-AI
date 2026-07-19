
import datetime

from core.constants.underlyings import NIFTY
from services.option_chain_service import OptionChainService


analysis = OptionChainService()
option_analysis = analysis.get_option_chain(NIFTY,expiry_date="2026-07-21")

print("Analysis Summary:")
print(option_analysis)