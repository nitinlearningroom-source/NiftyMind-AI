from core.analyzer.base_option_analyzer import BaseOptionAnalyzer
from core.models.models import OptionAnalysisConfig, Unserlying_SentimentSnapshot
from option_chain.models.option_analysis import OptionAnalysis
from option_chain.models.option_chain_snapshot import OptionSnapshot
from option_chain.models.option_contract import OptionContract


class Option_Analyzer(BaseOptionAnalyzer):

    def __init__(self, config: OptionAnalysisConfig):
        super().__init__(config)

    def analyze(self, snapshot: Unserlying_SentimentSnapshot) -> OptionAnalysis:

        option_chain = snapshot.option_chain
        
        calls = [c for c in option_chain.contracts if c.option_type.upper() == "CALL"]
        puts = [p for p in option_chain.contracts if p.option_type.upper() == "PUT"]

        if not calls or not puts:
            raise ValueError("Option chain does not contain both CALL and PUT contracts.")

        # -------------------------
        # ATM Strike
        # -------------------------
        atm_strike = min(
            {c.strike for c in option_chain.contracts},
            key=lambda strike: abs(strike - snapshot.spot_price)
        )

        atm_call = next(
            c for c in calls if c.strike == atm_strike
        )

        atm_put = next(
            p for p in puts if p.strike == atm_strike
        )

        # -------------------------
        # Support & Resistance
        # -------------------------

        support_contract = max(puts, key=lambda x: x.oi)
        resistance_contract = max(calls, key=lambda x: x.oi)

        support = support_contract.strike
        resistance = resistance_contract.strike

        # -------------------------
        # PCR
        # -------------------------

        total_call_oi = sum(c.oi for c in calls)
        total_put_oi = sum(p.oi for p in puts)

        pcr = (
            total_put_oi / total_call_oi
            if total_call_oi > 0
            else 0
        )

        # -------------------------
        # ITM / OTM
        # -------------------------

        itm_calls = [
            c for c in calls
            if c.strike < snapshot.spot_price
        ]

        otm_calls = [
            c for c in calls
            if c.strike > snapshot.spot_price
        ]

        itm_puts = [
            p for p in puts
            if p.strike > snapshot.spot_price
        ]

        otm_puts = [
            p for p in puts
            if p.strike < snapshot.spot_price
        ]

        # -------------------------
        # Market Bias
        # -------------------------

        bullish = False
        bearish = False
        sideways = False

        if pcr > 1.10:
            bullish = True

        elif pcr < 0.90:
            bearish = True

        else:
            sideways = True

        summary = (
            f"ATM={atm_strike}, "
            f"PCR={pcr:.2f}, "
            f"Support={support}, "
            f"Resistance={resistance}"
        )

        return OptionAnalysis(
            underlying=snapshot.underlying,
            expiry=snapshot.expiry,
            spot_price=snapshot.spot_price,
            atm_strike=atm_strike,
            atm_call=atm_call,
            atm_put=atm_put,
            itm_calls=itm_calls,
            itm_puts=itm_puts,
            otm_calls=otm_calls,
            otm_puts=otm_puts,
            support=support,
            resistance=resistance,
            pcr=pcr,
            max_call_oi=resistance_contract.oi,
            max_put_oi=support_contract.oi,
            max_call_oi_strike=resistance_contract.strike,
            max_put_oi_strike=support_contract.strike,
            bullish=bullish,
            bearish=bearish,
            sideways=sideways,
            summary=summary
        )