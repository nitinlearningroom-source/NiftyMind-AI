from dataclasses import dataclass


@dataclass
class OIAnalysis:
    total_call_oi: int
    total_put_oi: int

    total_call_change_oi: int
    total_put_change_oi: int

    max_call_oi_strike: float
    max_put_oi_strike: float

    support: float
    resistance: float

    support_strength: float
    resistance_strength: float

    call_writing: bool
    put_writing: bool

    trend: str