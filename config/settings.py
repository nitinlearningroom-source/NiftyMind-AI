from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"

DEFAULT_RSI = 14

DEFAULT_ATR = 14

DEFAULT_BB_PERIOD = 20

DEFAULT_BB_STD = 2

EMA_PERIODS = [5, 20, 50, 100, 200]

MACD = {
    "FAST": 12,
    "SLOW": 26,
    "SIGNAL": 9,
}
