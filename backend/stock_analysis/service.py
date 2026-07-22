from __future__ import annotations

from .config import SIGNAL_THRESHOLDS
from .data_fetcher import clean_ticker, load_stock_data
from .indicators import add_indicators, indicator_reasons, prepare_chart_data
from .ml_models import train_lstm_model, train_trend_model
from .risk import calculate_risk_score
from .signals import combine_final_signal, market_trend_label, xgboost_outlook_label


def analyze_ticker(ticker: str, period: str, interval: str, refresh: bool) -> dict:
    ticker = clean_ticker(ticker)
    raw = load_stock_data(ticker, period, interval, refresh)
    if raw.empty:
        raise ValueError(f"No market data found for {ticker}.")

    df = add_indicators(raw)
    _xgb_model, xgb_accuracy, _latest_features, trend_probability = train_trend_model(df)
    _lstm_model, lstm_trend = train_lstm_model(df, SIGNAL_THRESHOLDS.lstm_move_pct)

    latest = df.iloc[-1]
    previous = df.iloc[-2]
    price_change_pct = ((latest["Close"] - previous["Close"]) / previous["Close"]) * 100
    risk_score = calculate_risk_score(latest)
    signal_reasons = indicator_reasons(latest)
    market_trend = market_trend_label(latest, SIGNAL_THRESHOLDS.market_trend_gap_pct)
    xgb_outlook = xgboost_outlook_label(trend_probability, SIGNAL_THRESHOLDS)
    final_signal, weighted_score, final_reasons = combine_final_signal(
        market_trend,
        lstm_trend,
        trend_probability,
        risk_score,
        SIGNAL_THRESHOLDS,
    )

    return {
        "ticker": ticker,
        "finalSignal": final_signal,
        "weightedScore": weighted_score,
        "marketTrend": market_trend,
        "lstmTrend": lstm_trend.direction,
        "lstmMovePct": lstm_trend.move_pct,
        "bullishProbability": round(trend_probability * 100, 1),
        "riskScore": risk_score,
        "xgbOutlook": xgb_outlook,
        "priceChangePct": round(price_change_pct, 2),
        "rows": len(df),
        "accuracy": round(xgb_accuracy * 100, 1),
        "signalReasons": final_reasons,
        "indicatorReasons": signal_reasons,
        "chartData": prepare_chart_data(df.tail(120)),
    }
