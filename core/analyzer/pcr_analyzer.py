from Options_Rules.enums import PCRSignal
from core.analyzer.base_option_analyzer import BaseOptionAnalyzer
from core.models.models import OptionAnalysisConfig, PCRAnalysis, Unserlying_SentimentSnapshot


class PCRAnalyzer(BaseOptionAnalyzer):

    def __init__(self, config: OptionAnalysisConfig):
        super().__init__(config)

    def analyze(
        self,
        snapshot: Unserlying_SentimentSnapshot
    ) -> PCRAnalysis:
        
        df = self.get_option_chain(snapshot)
        
        spot = snapshot.spot_price
        self.validate_columns(df, [
            "call_oi",
            "put_oi"
        ])
        
        filtered_df = self.filter_atm_window(df=df,spot_price=spot)

        total_call_oi = filtered_df["call_oi"].sum()
        total_put_oi = filtered_df["put_oi"].sum()
        pcr = total_put_oi / total_call_oi
        if total_call_oi == 0:
            raise ValueError("Total Call OI cannot be zero.")
        
        signal, interpretation = self._interpret(pcr)

        return PCRAnalysis(
            value=round(pcr, 2),
            signal=signal,
            interpretation=interpretation,
        )
        
        
    def _interpret(self, pcr: float):
        if pcr < 0.70:
            return PCRSignal.BEARISH,"Excessive Call OI"

        if pcr < 0.90:
            return PCRSignal.SLIGHTLY_BEARISH, "Moderate bearish positioning"

        if pcr <= 1.10:
            return PCRSignal.NEUTRAL, "Balanced positioning"

        if pcr <= 1.30:
            return PCRSignal.BULLISH, "Strong Put positioning"

        return PCRSignal.BULLISH, "Heavy Put positioning"