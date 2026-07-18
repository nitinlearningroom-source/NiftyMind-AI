from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"
# EMA
EMA_PERIODS = [20, 50, 100, 200]

# RSI
RSI_LENGTH = 14

# MACD
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# ATR
ATR_LENGTH = 14

# Bollinger Bands
BB_LENGTH = 20
BB_STD = 2.0

# SuperTrend
SUPERTREND_LENGTH = 10
SUPERTREND_MULTIPLIER = 3.0

# ADX
ADX_LENGTH = 14

# Stochastic RSI
STOCH_RSI_LENGTH = 14
STOCH_RSI_RSI_LENGTH = 14
STOCH_RSI_K = 3
STOCH_RSI_D = 3

# Donchian Channel
DONCHIAN_LENGTH = 20