from __future__ import annotations

import pandas as pd

from .config import SignalThresholds
from .ml_models import LstmTrend


def market_trend_label(latest: pd.Series, min_gap_pct: float) -> str:
    sma_gap_pct = ((latest["SMA_20"] - latest["SMA_50"]) / latest["SMA_50"]) * 100
    close_gap_pct = ((latest["Close"] - latest["SMA_20"]) / latest["SMA_20"]) * 100
    if sma_gap_pct >= min_gap_pct and close_gap_pct >= min_gap_pct:
        return "UPTREND"
    if sma_gap_pct <= -min_gap_pct and close_gap_pct <= -min_gap_pct:
        return "DOWNTREND"
    return "SIDEWAYS"


def xgboost_outlook_label(trend_probability: float, thresholds: SignalThresholds) -> str:
    if trend_probability >= thresholds.xgb_bullish:
        return "Bullish"
    if trend_probability <= thresholds.xgb_bearish:
        return "Bearish"
    return "Neutral"


def combine_final_signal(
    market_trend: str,
    lstm_trend: LstmTrend,
    trend_probability: float,
    risk_score: float,
    thresholds: SignalThresholds,
) -> tuple[str, int, list[str]]:
    score = 0
    reasons: list[str] = []
    if market_trend == "UPTREND":
        score += 2
        reasons.append("Market trend adds +2 because price and moving averages confirm an uptrend.")
    elif market_trend == "DOWNTREND":
        score -= 2
        reasons.append("Market trend adds -2 because price and moving averages confirm a downtrend.")
    else:
        reasons.append("Market trend adds 0 because the chart is sideways.")
    if lstm_trend.move_pct >= thresholds.lstm_strong_move_pct:
        score += 2
        reasons.append(f"LSTM adds +2 because forecast move is strong at {lstm_trend.move_pct:+.2f}%.")
    elif lstm_trend.move_pct >= thresholds.lstm_move_pct:
        score += 1
        reasons.append(f"LSTM adds +1 because forecast move is mildly bullish at {lstm_trend.move_pct:+.2f}%.")
    elif lstm_trend.move_pct <= -thresholds.lstm_strong_move_pct:
        score -= 2
        reasons.append(f"LSTM adds -2 because forecast move is strongly bearish at {lstm_trend.move_pct:+.2f}%.")
    elif lstm_trend.move_pct <= -thresholds.lstm_move_pct:
        score -= 1
        reasons.append(f"LSTM adds -1 because forecast move is mildly bearish at {lstm_trend.move_pct:+.2f}%.")
    else:
        reasons.append(f"LSTM adds 0 because forecast move is inside the flat threshold at {lstm_trend.move_pct:+.2f}%.")
    if trend_probability >= thresholds.xgb_strong:
        score += 2
        reasons.append(f"XGBoost adds +2 because bullish probability is strong at {trend_probability * 100:.1f}%.")
    elif trend_probability >= thresholds.xgb_bullish:
        score += 1
        reasons.append(f"XGBoost adds +1 because bullish probability is positive at {trend_probability * 100:.1f}%.")
    elif trend_probability <= 1 - thresholds.xgb_strong:
        score -= 2
        reasons.append(f"XGBoost adds -2 because bullish probability is very low at {trend_probability * 100:.1f}%.")
    elif trend_probability <= thresholds.xgb_bearish:
        score -= 1
        reasons.append(f"XGBoost adds -1 because bullish probability is weak at {trend_probability * 100:.1f}%.")
    else:
        reasons.append(f"XGBoost adds 0 because bullish probability is neutral at {trend_probability * 100:.1f}%.")
    if score >= 3:
        if risk_score >= thresholds.max_buy_risk:
            reasons.append(f"Final score is +{score}, but risk score {risk_score}/100 is too high for BUY.")
            return "HOLD", score, reasons
        if score >= 5:
            reasons.append(f"Final weighted score is +{score}, so signals are strongly bullish.")
            return "STRONG BUY", score, reasons
        reasons.append(f"Final weighted score is +{score}, so signals are bullish.")
        return "BUY", score, reasons
    if score <= -3:
        if score <= -5:
            reasons.append(f"Final weighted score is {score}, so signals are strongly bearish.")
            return "STRONG SELL", score, reasons
        reasons.append(f"Final weighted score is {score}, so signals are bearish.")
        return "SELL", score, reasons
    reasons.append(f"Final weighted score is {score}, which is not strong enough for BUY or SELL.")
    return "HOLD", score, reasons
