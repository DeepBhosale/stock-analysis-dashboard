from __future__ import annotations

import numpy as np
import pandas as pd


def add_indicators(data: pd.DataFrame) -> pd.DataFrame:
    df = data.copy()
    df["SMA_20"] = df["Close"].rolling(20).mean()
    df["SMA_50"] = df["Close"].rolling(50).mean()
    df["EMA_20"] = df["Close"].ewm(span=20, adjust=False).mean()
    df["EMA_50"] = df["Close"].ewm(span=50, adjust=False).mean()

    delta = df["Close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(14).mean()
    avg_loss = loss.rolling(14).mean()
    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    ema12 = df["Close"].ewm(span=12, adjust=False).mean()
    ema26 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]

    df["Daily_Return"] = df["Close"].pct_change()
    df["Volatility_20"] = df["Daily_Return"].rolling(20).std() * np.sqrt(252)
    df["Volume_Change"] = df["Volume"].pct_change()
    df["Momentum_5"] = df["Close"] - df["Close"].shift(5)
    df["Momentum_10"] = df["Close"] - df["Close"].shift(10)

    rolling_mean = df["Close"].rolling(20).mean()
    rolling_std = df["Close"].rolling(20).std()
    df["BB_Upper"] = rolling_mean + (2 * rolling_std)
    df["BB_Lower"] = rolling_mean - (2 * rolling_std)
    df["BB_Width"] = (df["BB_Upper"] - df["BB_Lower"]) / rolling_mean

    df["HighLowRange"] = (df["High"] - df["Low"]) / df["Close"]
    df["CloseOpenDiff"] = (df["Close"] - df["Open"]) / df["Open"]
    df["Return_1"] = df["Close"].pct_change(1)
    df["Return_3"] = df["Close"].pct_change(3)
    df["Return_5"] = df["Close"].pct_change(5)

    future_return = df["Close"].shift(-5) / df["Close"] - 1
    df["Target"] = np.where(future_return > 0.02, 1, 0)
    return df.dropna()


def indicator_reasons(latest: pd.Series) -> list[str]:
    reasons: list[str] = []
    if latest["SMA_20"] > latest["SMA_50"]:
        reasons.append("SMA 20 is above SMA 50")
    else:
        reasons.append("SMA 20 is below SMA 50")
    if latest["MACD"] > latest["MACD_Signal"]:
        reasons.append("MACD is above signal line")
    else:
        reasons.append("MACD is below signal line")
    if latest["RSI"] < 30:
        reasons.append("RSI shows oversold conditions")
    elif latest["RSI"] > 70:
        reasons.append("RSI shows overbought conditions")
    else:
        reasons.append("RSI is in a balanced range")
    return reasons


def prepare_chart_data(df: pd.DataFrame) -> dict:
    return {
        "dates": df.index.strftime("%Y-%m-%d").tolist(),
        "open": df["Open"].round(2).tolist(),
        "high": df["High"].round(2).tolist(),
        "low": df["Low"].round(2).tolist(),
        "close": df["Close"].round(2).tolist(),
        "sma20": df["SMA_20"].round(2).tolist(),
        "sma50": df["SMA_50"].round(2).tolist(),
        "rsi": df["RSI"].round(2).tolist(),
        "macd": df["MACD"].round(3).tolist(),
        "macdSignal": df["MACD_Signal"].round(3).tolist(),
        "macdHist": df["MACD_Hist"].round(3).tolist(),
    }
