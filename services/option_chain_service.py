from __future__ import annotations

import json
import logging
from datetime import datetime
import pandas as pd
from pprint import pprint
from brokers.dhanhq.auth import DhanClient
from core.models.models import OptionChainSnapshot
from core.models.underlying import Underlying



logger = logging.getLogger(__name__)


class OptionChainService:
    """
    Service responsible for retrieving and normalizing
    Option Chain data from Dhan.

    Responsibilities:
        • Call Dhan API
        • Validate response
        • Normalize into DataFrame
        • Return broker-independent data
    """

    def __init__(self):
        self.client = DhanClient().client

    def get_option_chain(
        self,
        underlying: Underlying,
        expiry_date: str,
    ) -> OptionChainSnapshot:

        try:

            #expiries = self.client.expiry_list(under_security_id=13, under_exchange_segment="IDX_I")
            #print(expiries)
  

            response = self.client.option_chain(
                under_security_id= underlying.security_id,
                under_exchange_segment=underlying.exchange_segment,
                expiry=expiry_date
            )
            print(response)
           # return self._normalize_response(response=response, expiry=expiry_date, underlying=underlying)

        except Exception as ex:
            logger.exception("Failed to fetch option chain.")
            raise ex

    # ----------------------------------------------------

    def _normalize_response(self, 
                            response: any, 
                            expiry: str, 
                            underlying:Underlying):

          if response.get("status") != "success":
               raise ValueError(response.get("remarks", "API Error"))

          payload = response.get("data", {})

          # Dhan sometimes nests data inside another "data"
          if "data" in payload:
               payload = payload["data"]

          spot_price = payload.get("last_price")

          if spot_price is None:
               raise ValueError("Spot price not found in response.")
          
          option_chain = payload.get("oc", {})

          if not option_chain:
               raise ValueError("Option Chain not found.")

          rows = []

          for strike, option in option_chain.items():

               ce = option.get("ce", {})
               pe = option.get("pe", {})

               call_greeks = ce.get("greeks", {})
               put_greeks = pe.get("greeks", {})
               rows.append({
                    "strike": float(strike),

                    "call_security_id": ce.get("security_id"),
                    "call_oi": ce.get("oi", 0),
                    "call_previous_oi": ce.get("previous_oi", 0),
                    "call_change_oi": ce.get("oi", 0) - ce.get("previous_oi", 0),
                    "call_volume": ce.get("volume", 0),
                    "call_iv": ce.get("implied_volatility", 0),
                    "call_ltp": ce.get("last_price", 0),

                    "put_security_id": pe.get("security_id"),
                    "put_oi": pe.get("oi", 0),
                    "put_previous_oi": pe.get("previous_oi", 0),
                    "put_change_oi": pe.get("oi", 0) - pe.get("previous_oi", 0),
                    "put_volume": pe.get("volume", 0),
                    "put_iv": pe.get("implied_volatility", 0),
                    "put_ltp": pe.get("last_price", 0),
                    "call_delta": call_greeks.get("delta", 0),
                    "call_gamma": call_greeks.get("gamma", 0),
                    "call_theta": call_greeks.get("theta", 0),
                    "call_vega": call_greeks.get("vega", 0),

                    "put_delta": put_greeks.get("delta", 0),
                    "put_gamma": put_greeks.get("gamma", 0),
                    "put_theta": put_greeks.get("theta", 0),
                    "put_vega": put_greeks.get("vega", 0)

               })

          df = pd.DataFrame(rows)
          df = df.sort_values("strike").reset_index(drop=True)

          return OptionChainSnapshot(
               underlying=underlying,
               expiry=expiry,
               spot_price=spot_price,
               option_chain=df,
               timestamp=datetime.now(),
          )