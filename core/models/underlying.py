from dataclasses import dataclass

@dataclass(frozen=True)
class Underlying:
    name: str
    security_id: int
    exchange_segment: str