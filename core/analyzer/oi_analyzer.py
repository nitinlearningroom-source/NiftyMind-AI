from core.analyzer.base_option_analyzer import BaseOptionAnalyzer
from core.constants.enums import OITrend
from core.models.models import OIAnalysis,  OptionAnalysisConfig, Unserlying_SentimentSnapshot


class OIAnalyzer(BaseOptionAnalyzer):
            
    def __init__(self, config: OptionAnalysisConfig):
        super().__init__(config)

    def analyze(
        self,
        snapshot: Unserlying_SentimentSnapshot
    ) -> OIAnalysis:

        df = self.get_option_chain(snapshot)

        self.validate_columns(df, [
            "call_oi",
            "put_oi",
            "call_change_oi",
            "put_change_oi",
            "strike"
        ])

        totals = self._calculate_totals(df)

        support = self._calculate_support(df)

        resistance = self._calculate_resistance(df)

        writing = self._detect_writing(totals)

        trend = self._determine_trend(writing)

        return OIAnalysis(
            total_call_oi=totals["call_oi"],
            total_put_oi=totals["put_oi"],
            total_call_change_oi=totals["call_change"],
            total_put_change_oi=totals["put_change"],

            support=support["strike"],
            support_strength=support["strength"],

            resistance=resistance["strike"],
            resistance_strength=resistance["strength"],

            max_call_oi_strike=resistance["strike"],
            max_put_oi_strike=support["strike"],


            call_writing=writing["call"],
            put_writing=writing["put"],

            trend=trend
        )
    
    def _calculate_totals(self, df):
        return {

            "call_oi": int(df["call_oi"].sum()),

            "put_oi": int(df["put_oi"].sum()),

            "call_change": int(df["call_change_oi"].sum()),

            "put_change": int(df["put_change_oi"].sum())
        }
    
    def _calculate_support(self, df):

        row = df.loc[df["put_oi"].idxmax()]

        return {

            "strike": float(row["strike"]),

            "strength": int(row["put_oi"])
        }
    
    def _calculate_resistance(self, df):
        row = df.loc[df["call_oi"].idxmax()]

        return {

            "strike": float(row["strike"]),

            "strength": int(row["call_oi"])
        }
    
    def _detect_writing(self, totals):

        return {

            "call": totals["call_change"] > 0,

            "put": totals["put_change"] > 0
        }
    
    def _determine_trend(self, writing):

        if writing["put"] and not writing["call"]:
            return OITrend.BULLISH

        if writing["call"] and not writing["put"]:
            return OITrend.BEARISH  

        return OITrend.NEUTRAL
    
