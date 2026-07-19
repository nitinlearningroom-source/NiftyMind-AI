from core.analyzer.enums import OITrend
from core.analyzer.models import OIAnalysis


class OIAnalyzer:

    def __init__(self, df):
        self.df = df

    def analyze(self) -> OIAnalysis:
        """
        Analyze Open Interest data and return an OIAnalysis object.
        """
        # Calculate total open interest for calls and puts
        total_call_oi = self.df["CALL_OI"].sum()
        total_put_oi = self.df["PUT_OI"].sum()

        total_call_change = self.df["call_change_oi"].sum()
        total_put_change = self.df["put_change_oi"].sum()

        support = self.df.loc[
            self.df["put_oi"].idxmax(),
            "strike"
        ]

        resistance = self.df.loc[
            self.df["call_oi"].idxmax(),
            "strike"
        ]
        call_writing = total_call_change > total_put_change
        put_writing = total_put_change > total_call_change


        if put_writing and not call_writing:
            trend = OITrend.BULLISH

        elif call_writing and not put_writing:
            trend = OITrend.BEARISH

        else:
            trend = OITrend.NEUTRAL

        # Calculate support level based on put OI
        support_oi = self.df["put_oi"].max()
        support_ratio = support_oi / total_put_oi
            
        if support_ratio >= 0.25:
            support_level = "STRONG"
        elif support_ratio >= 0.15:
            support_level = "MODERATE"
        else:
            support_level = "WEAK"

        # Calculate resistance level based on call OI
        resistance_oi = self.df["call_oi"].max()
        resistance_ratio = resistance_oi / total_call_oi        
        
        if resistance_ratio >= 0.25:
            resistance_level = "STRONG"
        elif resistance_ratio >= 0.15:
            resistance_level = "MODERATE"
        else:
            resistance_level = "WEAK"

        return OIAnalysis(
            total_call_oi=total_call_oi,
            total_put_oi=total_put_oi,
            total_call_change_oi=total_call_change,
            total_put_change_oi=total_put_change,
            support=support,
            resistance=resistance,
            call_writing=call_writing,
            put_writing=put_writing,
            trend=trend,
            support_strength=support_level,
            resistance_strength=resistance_level

        )