from core.constants.enums import Breakout, Momentum, Recommendation, Signal, Trend, TrendStrength, Volatility
from core.models.models import MarketAnalysis


class MarketAnalyzer:

    def __init__(self, indicator_engine):
        self.engine = indicator_engine

    def analyze_trend(self) -> Trend:
        summary = self.engine.summary()

        ema20 = summary.get("EMA_20")
        ema50 = summary.get("EMA_50")
        ema200 = summary.get("EMA_200")
        st = summary.get("SUPERTREND_DIRECTION")

        print(f"EMA20: {ema20}, EMA50: {ema50}, EMA200: {ema200}, SuperTrend: {st}")

        if ema20 is None or ema50 is None or st is None:
            return Trend.SIDEWAYS

        # Use EMA-200 when available
        if ema200 is not None:
            if ema20 > ema50 > ema200 and st == Signal.BUY.value:
                return Trend.BULLISH

            if ema20 < ema50 < ema200 and st == Signal.SELL.value:
                return Trend.BEARISH
        else:
            # Fallback when EMA-200 is unavailable
            if ema20 > ema50 and st == Signal.BUY.value:
                return Trend.BULLISH

            if ema20 < ema50 and st == Signal.SELL.value:
                return Trend.BEARISH

        return Trend.SIDEWAYS
    
    def analyze_trend_strength(self) -> TrendStrength:
        summary = self.engine.summary()

        adx = summary.get("ADX")

        if adx is None:
            return TrendStrength.WEAK

        if adx < 20:
            return TrendStrength.WEAK
        elif adx < 25:
            return TrendStrength.MODERATE
        elif adx < 40:
            return TrendStrength.STRONG
        else:
            return TrendStrength.VERY_STRONG
        
    def analyze_momentum(self):
        summary = self.engine.summary()

        rsi = summary.get("RSI")
        macd = summary.get("MACD")

        return {
            "RSI": rsi,
            "MACD": macd
        }
    
    def analyze_volatility(self):
        summary = self.engine.summary()

        atr = summary.get("ATR")
        bb_upper = summary.get("BB_UPPER")
        bb_lower = summary.get("BB_LOWER")

        return {
            "ATR": atr,
            "BB_UPPER": bb_upper,
            "BB_LOWER": bb_lower
        }
    
    def analyze_volume(self):
        summary = self.engine.summary()

        obv = summary.get("OBV")    
        vwap = summary.get("VWAP")

        return {
            "VWAP": vwap,
            "OBV": obv
        }
    
    def analyze_breakout(self):
        summary = self.engine.summary()

        pivot_points = summary.get("PIVOT_POINTS")
        donchian_upper = summary.get("DONCHIAN_UPPER")
        donchian_lower = summary.get("DONCHIAN_LOWER")

        return {
            "Pivot Points": pivot_points,
            "Donchian Upper": donchian_upper,
            "Donchian Lower": donchian_lower
        }
    
    def analyze_all(self):
        return {
            "trend": self.analyze_trend(),
            "trend_strength": self.analyze_trend_strength(),
            "momentum": self.analyze_momentum(),
            "volatility": self.analyze_volatility(),
            "volume": self.analyze_volume(),
            "breakout": self.analyze_breakout()
        }


    def generate_recommendation(
        self,
        bullish,
        bearish,
    ):
        if bullish >= 80 and bullish > bearish:
            return Recommendation.BUY_CALL

        if bearish >= 80 and bearish > bullish:
            return Recommendation.BUY_PUT

        return Recommendation.NO_TRADE
    
    def analyze(self):

        trend = self.analyze_trend()

        trend_strength = self.analyze_trend_strength()

        momentum = self.analyze_momentum()

        volume_confirmation = self.analyze_volume()

        breakout = self.analyze_breakout()

        volatility = self.analyze_volatility()

        result = self.calculate_confidence(
            trend,
            trend_strength,
            momentum,
            volume_confirmation,
            breakout,
            volatility
        )
        bullish, bearish = result

        recommendation = self.generate_recommendation(
            bullish,
            bearish
        )
        return MarketAnalysis(
            trend=trend,
            trend_strength=trend_strength,
            momentum=momentum,
            volume_confirmation=volume_confirmation,
            breakout=breakout,
            volatility=volatility,
            bullish_confidence=bullish,
            bearish_confidence=bearish,
            recommendation=recommendation
        )
            
    def calculate_confidence(
        self,
        trend,
        trend_strength,
        momentum,
        volume_confirmation,
        breakout,
        volatility
    ) -> tuple[int, int]:

        bullish = 0
        bearish = 0
        max_confidence = 100

        # Trend (30)
        if trend == Trend.BULLISH:
            bullish += 30

        elif trend == Trend.BEARISH:
            bearish += 30

        # Trend Strength (15)
        strength_score = {
            TrendStrength.WEAK: 0,
            TrendStrength.MODERATE: 5,
            TrendStrength.STRONG: 10,
            TrendStrength.VERY_STRONG: 15
        }

        bullish += strength_score.get(trend_strength, 0)
        bearish += strength_score.get(trend_strength, 0)

        # Momentum (20)
        if momentum == Momentum.BULLISH:
            bullish += 20
        elif momentum == Momentum.BEARISH:
            bearish += 20

        # Volume (10)
        if volume_confirmation:
            bullish += 10
            bearish += 10

        # Breakout (15)
        if breakout== Breakout.BULLISH :
            bullish += 15
        elif breakout == Breakout.BEARISH:
            bearish += 15

        # Volatility (10)
        if volatility == Volatility.NORMAL:
            bullish += 10
            bearish += 10
        elif volatility == Volatility.LOW:
            bullish += 5
            bearish += 5

        print(f"Confidence Scores - Bullish: {bullish}, Bearish: {bearish}")
        return bullish, bearish  