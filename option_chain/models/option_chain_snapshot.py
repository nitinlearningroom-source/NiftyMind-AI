from dataclasses import dataclass

from option_chain.models.option_contract import OptionContract


@dataclass(slots=True)
class OptionSnapshot:

    underlying: str

    expiry: str

    spot_price: float

    contracts: list[OptionContract]