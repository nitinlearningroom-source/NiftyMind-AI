from dataclasses import dataclass

from option_chain.models.option_contract import OptionContract


@dataclass(slots=True)
class OptionAnalysis:

    underlying: str

    spot_price: float

    expiry: str

    atm_strike: float

    atm_call: OptionContract

    atm_put: OptionContract

    itm_calls: list[OptionContract]

    itm_puts: list[OptionContract]

    otm_calls: list[OptionContract]

    otm_puts: list[OptionContract]

    support: float

    resistance: float

    pcr: float

    max_call_oi: int

    max_put_oi: int

    max_call_oi_strike: float

    max_put_oi_strike: float

    bullish: bool

    bearish: bool

    sideways: bool

    summary: str