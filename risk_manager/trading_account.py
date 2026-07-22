from dataclasses import dataclass

@dataclass(slots=True)
class TradingAccount:

    capital: float

    available_margin: float

    used_margin: float

    todays_loss: float

    open_positions: int

    max_open_positions: int