from dataclasses import dataclass


@dataclass(slots=True)
class OptionContract:
    symbol: str

    strike: float

    option_type: str          # CALL / PUT

    expiry: str

    security_id: str

    ltp: float

    bid: float

    ask: float

    volume: int

    oi: int

    previous_oi: int

    oi_change: int

    iv: float | None = None

    delta: float | None = None

    gamma: float | None = None

    theta: float | None = None

    vega: float | None = None   