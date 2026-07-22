from dataclasses import dataclass

@dataclass(slots=True)
class PositionSize:

    quantity: int

    lots: int

    capital_required: float

    max_loss: float