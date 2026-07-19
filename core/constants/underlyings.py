

import core.models.underlying


NIFTY = core.models.underlying.Underlying(
    name="NIFTY",
    security_id=13,
    exchange_segment="IDX_I"
)

BANKNIFTY = core.models.underlying.Underlying(
    name="BANKNIFTY",
    security_id=25,
    exchange_segment="IDX_I"
)

FINNIFTY = core.models.underlying.Underlying(
    name="FINNIFTY",
    security_id=27,
    exchange_segment="IDX_I"
)

MIDCPNIFTY = core.models.underlying.Underlying(
    name="MIDCPNIFTY",
    security_id=442,
    exchange_segment="IDX_I"
)

SENSEX = core.models.underlying.Underlying(
    name="SENSEX",
    security_id=51,
    exchange_segment="IDX_I"
)

BANKEX = core.models.underlying.Underlying(
    name="BANKEX",
    security_id=69,
    exchange_segment="IDX_I"
)