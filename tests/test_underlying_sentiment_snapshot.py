from datetime import datetime

import pandas as pd

from core.models.models import Unserlying_SentimentSnapshot
from core.models.underlying import Underlying


def test_snapshot_round_trip_serialization():
    snapshot = Unserlying_SentimentSnapshot(
        underlying=Underlying(name="NIFTY", security_id=13, exchange_segment="IDX_I"),
        expiry="2026-07-28",
        spot_price=22500.0,
        timestamp=datetime(2026, 7, 22, 12, 0, 0),
        option_chain=pd.DataFrame([{"strike": 22000.0, "call_oi": 1000}]),
    )

    payload = snapshot.to_dict()

    restored = Unserlying_SentimentSnapshot.from_dict(payload)

    assert restored.expiry == snapshot.expiry
    assert restored.spot_price == snapshot.spot_price
    assert restored.underlying.name == snapshot.underlying.name
    assert restored.option_chain.iloc[0]["call_oi"] == 1000
    assert restored.timestamp == snapshot.timestamp
