from enum import Enum

class InstrumentType(Enum):
    EQUITY = "EQUITY"
    INDEX = "INDEX"
    FUTURE = "FUTURE"
    OPTION = "OPTION"
    ETF = "ETF"
    CURRENCY = "CURRENCY"
    COMMODITY = "COMMODITY"