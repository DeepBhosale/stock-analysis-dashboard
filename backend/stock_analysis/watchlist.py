from __future__ import annotations

import numpy as np

from .config import COMPANY_NAMES
from .data_fetcher import clean_ticker, fetch_stock_data

def fetch_live_watchlist_data(tickers: list[str]) -> list[dict]:
    stocks = []
    for ticker in tickers:
        ticker = clean_ticker(ticker)
        stock_df = fetch_stock_data(ticker, period="6mo", interval="1d")
        if stock_df.empty or len(stock_df) < 2:
            continue

        latest = stock_df.iloc[-1]
        prev = stock_df.iloc[-2]
        price = float(latest.Close)
        change_pct = float((price - float(prev.Close)) / float(prev.Close) * 100)

        sma20 = stock_df["Close"].rolling(20).mean().iloc[-1] if len(stock_df) >= 20 else np.nan
        sma50 = stock_df["Close"].rolling(50).mean().iloc[-1] if len(stock_df) >= 50 else np.nan
        if not np.isnan(sma20) and not np.isnan(sma50):
            if price > sma20 and sma20 > sma50:
                final_signal = "Buy"
                market_trend = "Bullish"
            elif price < sma20 and sma20 < sma50:
                final_signal = "Sell"
                market_trend = "Bearish"
            else:
                final_signal = "Hold"
                market_trend = "Neutral"
        else:
            final_signal = "Hold"
            market_trend = "Neutral"

        bullish_probability = int(min(max(50 + change_pct * 1.5, 20), 80))
        risk_score = int(min(max(50 + ((sma50 - price) / price * 100) if not np.isnan(sma50) else 50, 20), 85))
        notes = f"{ticker} watchlist signal is based on recent price action and moving averages."

        stocks.append(
            {
                "ticker": ticker,
                "name": COMPANY_NAMES.get(ticker, ticker),
                "price": f"{price:.2f}",
                "change": f"{change_pct:+.2f}%",
                "finalSignal": final_signal,
                "marketTrend": market_trend,
                "bullishProbability": bullish_probability,
                "riskScore": risk_score,
                "notes": notes,
            }
        )

    return stocks
