from __future__ import annotations

import json
import logging
from datetime import datetime
import pandas as pd
from pprint import pprint
from brokers.dhanhq.auth import DhanClient
from core.models.models import Unserlying_SentimentSnapshot
from core.models.underlying import Underlying
from option_chain.models.option_chain_snapshot import OptionSnapshot
from option_chain.models.option_contract import OptionContract



logger = logging.getLogger(__name__)


class Underlying_Sentiments_Service:
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

    def _get_option_chain(
        self,
        underlying: Underlying,
        expiry_date: str,
        
    ) -> Unserlying_SentimentSnapshot:

        try:
            response = self.client.option_chain(
                under_security_id= underlying.security_id,
                under_exchange_segment=underlying.exchange_segment,
                expiry=expiry_date
            )
            print(f"response_Data length : {response} \n Input Data: Id {underlying.security_id} , segment : {underlying.exchange_segment} , expiry : {expiry_date}")
            return response

        except Exception as ex:
            logger.exception("Failed to fetch option chain.")
            raise ex

    # ----------------------------------------------------
    def Get_Sentiment_OptionData(self,
            underlying: Underlying,
            expiry_date: str,
            )-> Unserlying_SentimentSnapshot:
          response_data =self._get_option_chain(underlying=underlying,expiry_date=expiry_date)
          
          return self._normalize_response(response=response_data, expiry=expiry_date, underlying=underlying)
     
 
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
          
          option_data = self.Get_Option_Chanin(response_data=response,underlying=underlying.name,expiry_date=expiry)
          
          return Unserlying_SentimentSnapshot(
               underlying=underlying,
               expiry=expiry,
               spot_price=spot_price,
               sentiment=df,
               option_chain=option_data,
               timestamp=datetime.now()
          )
          
    def Get_Option_Chanin(self,response_data,
            underlying: str,
            expiry_date: str,
            )-> OptionSnapshot:
          #response_data =self._get_option_chain(underlying=underlying,expiry_date=expiry_date)
          
          with open("Option_Chain_Data.json", "w") as file:
               json.dump(response_data, file, indent=4)
               
          spot_price = float(response_data["data"]["data"]["last_price"])
          
          contracts = []

          option_chain = response_data["data"]["data"]["oc"]

          for strike_str, option_data in option_chain.items():

               strike = float(strike_str)

               # Call Option
               contracts.append(
                    self._create_contract(
                    strike=strike,
                    option_type="CALL",
                    option_data=option_data["ce"],
                    expiry=expiry_date,
                    underlying=underlying
                    )
               )

               # Put Option
               contracts.append(
                    self._create_contract(
                    strike=strike,
                    option_type="PUT",
                    option_data=option_data["pe"],
                    expiry=expiry_date,
                    underlying=underlying
                    )
               )


          return OptionSnapshot(
               underlying=underlying,
               expiry=expiry_date or "",
               spot_price=float(spot_price),
               contracts=contracts
          )
    
    def _create_contract(
            self,
            strike: float,
            option_type: str,
            option_data: dict,
            expiry: str,
            underlying: str,
        ) -> OptionContract:
    
            return OptionContract(
                symbol=f"{underlying}_{expiry}_{int(strike)}_{option_type}",
                security_id=str(option_data["security_id"]),
                strike=strike,
                option_type=option_type,
                expiry=expiry,
    
                ltp=float(option_data["last_price"]),
    
                bid=float(option_data["top_bid_price"]),
                ask=float(option_data["top_ask_price"]),
    
                volume=int(option_data["volume"]),
    
                oi=int(option_data["oi"]),
    
                previous_oi=int(option_data.get("previous_oi", 0)),
    
                oi_change=int(option_data["oi"]) - int(option_data.get("previous_oi", 0)),
    
                iv=float(option_data.get("implied_volatility", 0.0)),
    
                delta=float(option_data["greeks"].get("delta", 0.0)),
                gamma=float(option_data["greeks"].get("gamma", 0.0)),
                theta=float(option_data["greeks"].get("theta", 0.0)),
                vega=float(option_data["greeks"].get("vega", 0.0)),
            )