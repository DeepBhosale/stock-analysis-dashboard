from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
LEGACY_MARKET_CSV_PATH = DATA_DIR / "market_data.csv"
DATA_DIR.mkdir(exist_ok=True)

APP_VERSION = "React/Vite UI + FastAPI Backend"

XGB_BULLISH = 65
XGB_BEARISH = 35
LSTM_MOVE = 1.0
STRONG_LSTM = 3.0
TREND_GAP = 0.5
MAX_BUY_RISK = 70
STRONG_XGB = 75

COMPANY_NAMES = {
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "TSLA": "Tesla",
    "NVDA": "NVIDIA",
    "AMZN": "Amazon",
}


@dataclass(frozen=True)
class SignalThresholds:
    xgb_bullish: float
    xgb_bearish: float
    xgb_strong: float
    lstm_move_pct: float
    lstm_strong_move_pct: float
    market_trend_gap_pct: float
    max_buy_risk: float


SIGNAL_THRESHOLDS = SignalThresholds(
    xgb_bullish=XGB_BULLISH / 100,
    xgb_bearish=XGB_BEARISH / 100,
    xgb_strong=STRONG_XGB / 100,
    lstm_move_pct=LSTM_MOVE,
    lstm_strong_move_pct=STRONG_LSTM,
    market_trend_gap_pct=TREND_GAP,
    max_buy_risk=MAX_BUY_RISK,
)
