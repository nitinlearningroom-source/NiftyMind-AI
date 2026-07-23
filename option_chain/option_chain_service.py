import json

from brokers.dhanhq.auth import DhanClient

from core.models.underlying import Underlying
from option_chain.models.option_chain_snapshot import OptionSnapshot
from option_chain.models.option_contract import OptionContract


class Option_Service:

    def __init__(self):
        self.dhan = DhanClient().get_client()

    def get_option_chain(
        self,
        underlying: Underlying,
        expiry_date: str,
    ) -> OptionSnapshot:

        print("hello")
        print(underlying.security_id,underlying.exchange_segment,expiry_date);
        response = self.dhan.option_chain(
                       under_security_id= underlying.security_id,
                       under_exchange_segment= underlying.exchange_segment,
                       expiry=expiry_date
                   )


        print("response option -" ,response)
        spot_price = float(response["data"]["data"]["last_price"])

        contracts = []

        option_chain = response["data"]["data"]["oc"]

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