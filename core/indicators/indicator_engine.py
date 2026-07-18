import pandas as pd
import pandas_ta_classic as ta
from core.indicators.momentum import MomentumIndicators
from core.indicators.volatility import VolatilityIndicators
from core.indicators.volume import VolumeIndicators
from core.indicators.trend import TrendIndicators
from core.constants import Signal, TrendStrength

class IndicatorEngine:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    @property
    def data(self):
        return self.df

    # -------------------------
    # EMA
    # -------------------------
    def ema(self, periods=None):

        if periods is None:
            periods = [20, 50, 100, 200]

        for period in periods:
            self.df[f"EMA_{period}"] = ta.ema(
                self.df["Close"],
                length=period
            )

        return self.df

    # -------------------------
    # RSI
    # -------------------------
    def rsi(self, period=14):

        self.df["RSI"] = ta.rsi(
            self.df["Close"],
            length=period
        )

        return self.df

    # -------------------------
    # MACD
    # -------------------------
    def macd(self):

        macd = ta.macd(self.df["Close"])

        self.df = pd.concat(
            [self.df, macd],
            axis=1
        )

        return self.df
    
    # -------------------------
    # ATR 
    # -------------------------
    
    def atr(self, period=14):
        """TODO: Implement ATR"""
        self.df = VolatilityIndicators(self.df).atr(period)
        return self.df
    
    #-------------------------
    # VWAP
    #-------------------------
    def vwap(self):
        self.df = VolumeIndicators(self.df).vwap()
        return self.df
    
    #-------------------------
    # Bollinger Bands
    #-------------------------

    def bollinger(self, period=20, std=2.0):
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

        self.df = pd.concat([self.df, bb], axis=1)
        return self.df
    
    #-------------------------
    # SuperTrend
    #-------------------------
    def supertrend(
            self,
            atr_period=10,
            multiplier=3
        ):

        self.df = TrendIndicators(self.df).supertrend(
            atr_period,
            multiplier
        )
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
    def adx(self, length=14):
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
    def stoch_rsi(self):
        self.df = MomentumIndicators(self.df).stoch_rsi()
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
    # Summary
    #-------------------------
    def summary(self):
        latest = self.df.iloc[-1]
        return {
            "Close": float(latest["Close"]),
            "EMA20": float(latest["EMA_20"]) if "EMA_20" in latest and not pd.isna(latest["EMA_20"]) else None,
            "EMA50": float(latest["EMA_50"]) if "EMA_50" in latest and not pd.isna(latest["EMA_50"]) else None,
            "RSI": float(latest["RSI"]) if "RSI" in latest and not pd.isna(latest["RSI"]) else None,
            "MACD": float(latest.get("MACD")) if "MACD" in latest and not pd.isna(latest["MACD"]) else None,
            "ATR": float(latest.get("ATR_14")) if "ATR_14" in latest and not pd.isna(latest["ATR_14"]) else None,
            "VWAP": float(latest.get("VWAP")) if "VWAP" in latest and not pd.isna(latest["VWAP"]) else None,
            "SuperTrend": float(latest.get("SUPERTREND")) if "SUPERTREND" in latest and not pd.isna(latest["SUPERTREND"]) else None,
            "ADX": float(latest.get("ADX")) if "ADX" in latest and not pd.isna(latest["ADX"]) else None,
            "Signal": self.supertrend_signal().value,
            "TrendStrength": self.adx_strength().value,
            "Stoch RSI K": float(latest["STOCH_RSI_K"]) if "STOCH_RSI_K" in latest and not pd.isna(latest["STOCH_RSI_K"]) else None,
            "Stoch RSI D": float(latest["STOCH_RSI_D"]) if "STOCH_RSI_D" in latest and not pd.isna(latest["STOCH_RSI_D"]) else None,
            "Momentum Signal": self.stoch_rsi_signal().value if "STOCH_RSI_K" in latest else None,
        }

    def calculate_all(self):
        self.ema()
        self.rsi()
        self.macd()
        self.atr()
        self.vwap()
        self.bollinger()
        self.supertrend()

        return self.df