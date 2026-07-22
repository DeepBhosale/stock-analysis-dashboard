from __future__ import annotations

import pandas as pd


def calculate_risk_score(latest: pd.Series) -> float:
    volatility = float(latest["Volatility_20"])
    rsi_risk = abs(float(latest["RSI"]) - 50) / 50
    return min(100, round((volatility * 55) + (rsi_risk * 30) + (abs(latest["Volume_Change"]) * 15), 1))
