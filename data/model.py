from dataclasses import dataclass

@dataclass(slots=True)
class Instrument:

    security_id: str
    symbol: str
    exchange_segment: str
    instrument_type: str

    exchange: str | None = None
    series: str | None = None
    lot_size: int = 1
    strike_price: float | None = None
    expiry_date: str | None = None
    option_type: str | None = None
