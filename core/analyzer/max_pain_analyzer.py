from core.analyzer.base_option_analyzer import BaseOptionAnalyzer
from core.models.models import MaxPainAnalysis, OptionAnalysisConfig


class MaxPainAnalyzer(BaseOptionAnalyzer):

    def __init__(self, config: OptionAnalysisConfig):
        super().__init__(config)
    
    REQUIRED_COLUMNS = [
    "strike",
    "call_oi",
    "put_oi"
    ]

    def analyze(self, snapshot):

        df = self.get_option_chain(snapshot)

        self.validate_columns(df, self.REQUIRED_COLUMNS)

        (
            strike,
            total_loss,
            call_loss,
            put_loss
        ) = self._calculate_max_pain(df)

        distance = strike - snapshot.spot_price

        return MaxPainAnalysis(
            max_pain_strike=strike,
            total_loss=round(total_loss, 2),
            call_loss=round(call_loss, 2),
            put_loss=round(put_loss, 2),
            distance_from_spot=round(distance, 2),
            market_bias=self._market_bias(distance)
        )
    
    def _calculate_max_pain(self, df):

        strikes = sorted(df["strike"].unique())

        minimum_loss = float("inf")

        best_strike = None

        best_call_loss = 0

        best_put_loss = 0

        for expiry in strikes:

            call_loss = self._calculate_call_loss(df, expiry)

            put_loss = self._calculate_put_loss(df, expiry)

            total = call_loss + put_loss

            if total < minimum_loss:

                minimum_loss = total

                best_strike = expiry

                best_call_loss = call_loss

                best_put_loss = put_loss

        return (
            best_strike,
            minimum_loss,
            best_call_loss,
            best_put_loss
        )
    
    def _calculate_call_loss(
        self,
        df,
        expiry_price
        ):

        loss = 0.0

        for _, row in df.iterrows():

            intrinsic = max(
                0,
                expiry_price - row["strike"]
            )

            loss += intrinsic * row["call_oi"]

        return loss
    
    def _calculate_put_loss(
        self,
        df,
        expiry_price
    ):

        loss = 0.0

        for _, row in df.iterrows():

            intrinsic = max(
                0,
                row["strike"] - expiry_price
            )

            loss += intrinsic * row["put_oi"]

        return loss
    
    def _market_bias(
        self,
        distance
    ):

        if abs(distance) < 50:
            return "NEUTRAL"

        if distance > 0:
            return "BULLISH"

        return "BEARISH"