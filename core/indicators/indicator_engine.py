import pandas as pd
import pandas_ta_classic as ta
from config import settings
from core.indicators.base_indicator import BaseIndicator
from core.indicators.momentum import MomentumIndicators
from core.indicators.support_resistance import SupportResistanceIndicators
from core.indicators.volatility import VolatilityIndicators
from core.indicators.volume import VolumeIndicators
from core.indicators.trend import TrendIndicators
from core.constants import  Signal, TrendStrength

class IndicatorEngine(BaseIndicator):


    @property
    def data(self):
        return self.df

    # -------------------------
    # EMA
    # -------------------------
    def ema(self, periods=None):

        if periods is None:
            periods = settings.EMA_PERIODS

        for period in periods:
            self.df[f"EMA_{period}"] = ta.ema(
                self.df["Close"],
                length=period
            )
        return self.df
         

    # -------------------------
    # RSI
    # -------------------------
    def rsi(self, period=None):

        if period is None:
            period = settings.RSI_LENGTH

        self.df = MomentumIndicators(self.df).rsi(period)
        self.logger.info("Calculating RSI for period: %s", period)
        return self.df

    # -------------------------
    # MACD
    # -------------------------
    def macd(
        self,
        fast: int = settings.MACD_FAST,
        slow: int = settings.MACD_SLOW,
        signal: int = settings.MACD_SIGNAL,
    ) -> pd.DataFrame:
        """
        Calculate the Moving Average Convergence Divergence (MACD).

        Args:
            fast: Fast EMA period.
            slow: Slow EMA period.
            signal: Signal line EMA period.

        Returns:
            DataFrame with MACD columns appended.
        """
        

        macd = ta.macd(
            close=self.df["Close"],
            fast=fast,
            slow=slow,
            signal=signal,
        )
        macd.columns = [
            "MACD",
            "MACD_HISTOGRAM",
            "MACD_SIGNAL",
        ]
        self._append_indicator(macd)
        self.logger.info("Calculating MACD with fast: %s, slow: %s, signal: %s", fast, slow, signal)
        return self.df
    
    # -------------------------
    # ATR 
    # -------------------------
    
    def atr(self, period=None):

        if period is None:
            period = settings.ATR_LENGTH

        self.df = VolatilityIndicators(self.df).atr(period)
        self.logger.info("Calculating ATR for period: %s", period)
        return self.df
    
    #-------------------------
    # VWAP
    #-------------------------
    def vwap(self):
        self.df = VolumeIndicators(self.df).vwap()
        self.logger.info("Calculating VWAP")
        return self.df
    
    #-------------------------
    # Bollinger Bands
    #-------------------------

    def bollinger(self, period=None, std=None):
        if period is None:
            period = settings.BB_LENGTH

        if std is None:
            std = settings.BB_STD

        bb = ta.bbands(
            close=self.df["Close"],
            length=period,
            std=std
        )

        bb = bb.rename(columns={
            bb.columns[0]: "BB_Lower",
            bb.columns[1]: "BB_Middle",
            bb.columns[2]: "BB_Upper",
            bb.columns[3]: "BB_Bandwidth",
            bb.columns[4]: "BB_Percent"
        })
        self._append_indicator(bb)
        self.logger.info("Calculating Bollinger Bands for period: %s, std: %s", period, std)
        return self.df
    
    #-------------------------
    # SuperTrend
    #-------------------------
    def supertrend(
            self,
            atr_period=None,
            multiplier=None
        ):

        if atr_period is None:
            atr_period = settings.SUPERTREND_LENGTH

        if multiplier is None:
            multiplier = settings.SUPERTREND_MULTIPLIER

        self.df = TrendIndicators(self.df).supertrend(
            atr_period,
            multiplier
        )
        self.logger.info("Calculating SuperTrend with atr_period: %s, multiplier: %s", atr_period, multiplier)
        return self.df
    
    #-------------------------
    # SuperTrend Signal - helper
    #-------------------------
    def supertrend_signal(self) -> str:
        latest = self.df.iloc[-1]
        if latest["SUPERTREND_DIRECTION"] == 1:
            return Signal.BUY

        return Signal.SELL
    #------------------------- 
    #ADX
    #-------------------------
    def adx(self, length=None):

        if length is None:
            length = settings.ADX_LENGTH

        self.df = TrendIndicators(self.df).adx(length)
        return self.df

   #-------------------------
    # ADX Strength - helper
    #-------------------------
    def adx_strength(self):

        latest = self.df.iloc[-1]

        adx = latest["ADX"]

        if adx < 20:
            return TrendStrength.SIDEWAYS

        elif adx < 25:
            return TrendStrength.WEAK_TREND

        elif adx < 40:
            return TrendStrength.STRONG_TREND

        else:
            return TrendStrength.VERY_STRONG_TREND

    #-------------------------
    # Stochastic RSI
    #-------------------------
    def stochastic_rsi(
        self,
        length: int = settings.STOCH_RSI_LENGTH,
        rsi_length: int = settings.STOCH_RSI_RSI_LENGTH,
        k: int = settings.STOCH_RSI_K,
        d: int = settings.STOCH_RSI_D,
    ):
        stoch = ta.stochrsi(
            close=self.df["Close"],
            length=length,
            rsi_length=rsi_length,
            k=k,
            d=d,
        )

        stoch.columns = [
            "STOCH_RSI_K",
            "STOCH_RSI_D",
        ]

        self._append_indicator(stoch)
        self.logger.info("Calculating Stochastic RSI for period: %s", length)
        return self.df

    #-------------------------
    # Stochastic RSI Signal - helper    
    #------------------------
    def stoch_rsi_signal(self):

        latest = self.df.iloc[-1]

        k = latest["STOCH_RSI_K"]
        d = latest["STOCH_RSI_D"]

        if k > d and k < 20:
            return Signal.BUY

        if k < d and k > 80:
            return Signal.SELL

        return Signal.HOLD

    #-------------------------
    #obv
    #-------------------------
    def obv(self):
        self.df = VolumeIndicators(self.df).obv()
        self.logger.info("Calculating OBV")
        return self.df
    
    #-------------------------
    # OBV Signal - helper
    #-------------------------
    def obv_signal(self):
        latest = self.df.iloc[-1]["OBV"]
        previous = self.df.iloc[-2]["OBV"]

        if latest > previous:
            return Signal.BUY

        elif latest < previous:
            return Signal.SELL

        return Signal.HOLD
    
    #-------------------------
    # Pivot Points  
    #-------------------------
    def pivot_points(self):

        self.df = SupportResistanceIndicators(
            self.df
        ).pivot_points()
        self.logger.info("Calculating Pivot Points")
        return self.df
    
    #-------------------------
    # Pivot Signal - helper
    #-------------------------
    def pivot_signal(self):

        latest = self.df.iloc[-1]

        close = latest["Close"]

        if close > latest["R1"]:
            return Signal.BUY

        elif close < latest["S1"]:
            return Signal.SELL

        return Signal.HOLD

    def donchian(self, length=None):
        if length is None:
            length = settings.DONCHIAN_LENGTH

        self.df = SupportResistanceIndicators(
            self.df
        ).donchian(length)
        self.logger.info("Calculating Donchian Channels for length: %s", length)
        return self.df
    
    #-------------------------
    # Donchian Signal - helper
    #-------------------------
    def donchian_signal(self):

        latest = self.df.iloc[-1]
        close = latest["Close"]

        upper = latest["DONCHIAN_UPPER"]
        lower = latest["DONCHIAN_LOWER"]

        if close > upper:
            return Signal.BUY

        elif close < lower:
            return Signal.SELL

        return Signal.HOLD
    
    #-------------------------
    # Summary
    #-------------------------
    def summary(self):
        self.logger.info("Generating summary")
        
        latest = self.df.iloc[-1]
        return {
            "Close": float(latest["Close"]),
            "EMA_20": float(latest["EMA_20"]) if "EMA_20" in latest and not pd.isna(latest["EMA_20"]) else None,
            "EMA_50": float(latest["EMA_50"]) if "EMA_50" in latest and not pd.isna(latest["EMA_50"]) else None,
            "EMA_200": float(latest["EMA_200"]) if "EMA_200" in latest and not pd.isna(latest["EMA_200"]) else None,
            "RSI": float(latest["RSI"]) if "RSI" in latest and not pd.isna(latest["RSI"]) else None,
            "MACD": float(latest.get("MACD")) if "MACD" in latest and not pd.isna(latest["MACD"]) else None,
            "ATR": float(latest.get("ATR_14")) if "ATR_14" in latest and not pd.isna(latest["ATR_14"]) else None,
            "VWAP": float(latest.get("VWAP")) if "VWAP" in latest and not pd.isna(latest["VWAP"]) else None,
            "SuperTrend": float(latest.get("SUPERTREND")) if "SUPERTREND" in latest and not pd.isna(latest["SUPERTREND"]) else None,
            "ADX": float(latest.get("ADX")) if "ADX" in latest and not pd.isna(latest["ADX"]) else None,
            "SUPERTREND_DIRECTION": self.supertrend_signal().value,
            "TrendStrength": self.adx_strength().value,
            "Stoch RSI K": float(latest["STOCH_RSI_K"]) if "STOCH_RSI_K" in latest and not pd.isna(latest["STOCH_RSI_K"]) else None,
            "Stoch RSI D": float(latest["STOCH_RSI_D"]) if "STOCH_RSI_D" in latest and not pd.isna(latest["STOCH_RSI_D"]) else None,
            "Momentum Signal": self.stoch_rsi_signal().value if "STOCH_RSI_K" in latest else None,
            "OBV": float(latest["OBV"]) if "OBV" in latest and not pd.isna(latest["OBV"]) else None,
            "OBV Signal": self.obv_signal().value if "OBV" in latest else None,
            "Pivot Points": {
                "Pivot": float(latest["PIVOT"]) if "PIVOT" in latest and not pd.isna(latest["PIVOT"]) else None,
                "R1": float(latest["R1"]) if "R1" in latest and not pd.isna(latest["R1"]) else None,
                "S1": float(latest["S1"]) if "S1" in latest and not pd.isna(latest["S1"]) else None,
                "R2": float(latest["R2"]) if "R2" in latest and not pd.isna(latest["R2"]) else None,
                "S2": float(latest["S2"]) if "S2" in latest and not pd.isna(latest["S2"]) else None,
                "R3": float(latest["R3"]) if "R3" in latest and not pd.isna(latest["R3"]) else None,
                "S3": float(latest["S3"]) if "S3" in latest and not pd.isna(latest["S3"]) else None,
                "Pivot Signal": self.pivot_signal().value
            },
            "Donchian": {
                "Upper": float(latest["DONCHIAN_UPPER"]) if "DONCHIAN_UPPER" in latest and not pd.isna(latest["DONCHIAN_UPPER"]) else None,
                "Lower": float(latest["DONCHIAN_LOWER"]) if "DONCHIAN_LOWER" in latest and not pd.isna(latest["DONCHIAN_LOWER"]) else None,
                "Middle": float(latest["DONCHIAN_MIDDLE"]) if "DONCHIAN_MIDDLE" in latest and not pd.isna(latest["DONCHIAN_MIDDLE"]) else None,
                "Donchian Signal": self.donchian_signal().value
            }
        }

    def calculate_all(self):
        self.donchian()
        self.obv()
        self.pivot_points()
        self.supertrend()
        self.ema()
        self.rsi()
        self.macd()
        self.atr()
        self.vwap()
        self.adx()
        self.stochastic_rsi()

        return self.df