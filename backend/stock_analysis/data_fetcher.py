from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests
import yfinance as yf

from .config import DATA_DIR, LEGACY_MARKET_CSV_PATH


def clean_ticker(value: str) -> str:
    return value.strip().upper()


def market_csv_path(ticker: str, period: str, interval: str) -> Path:
    cache_key = "_".join([clean_ticker(ticker), period, interval])
    safe_key = "".join(char if char.isalnum() else "_" for char in cache_key).strip("_")
    return DATA_DIR / f"market_data_{safe_key}.csv"


def normalize_download(data: pd.DataFrame) -> pd.DataFrame:
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    return data.rename(columns=str.title).dropna()


def prepare_market_data(data: pd.DataFrame) -> pd.DataFrame:
    data = normalize_download(data)
    required_columns = ["Open", "High", "Low", "Close", "Volume"]
    missing_columns = [column for column in required_columns if column not in data.columns]
    if data.empty or missing_columns:
        return pd.DataFrame()

    clean_data = data[required_columns].copy()
    clean_data.index = pd.to_datetime(clean_data.index)
    clean_data.index.name = "Date"
    return clean_data.sort_index()


def fetch_yahoo_chart_data(ticker: str, period: str, interval: str) -> pd.DataFrame:
    encoded_ticker = quote(ticker, safe="")
    url = (
        f"https://query1.finance.yahoo.com/v8/finance/chart/{encoded_ticker}"
        f"?range={period}&interval={interval}&includePrePost=false"
    )

    try:
        session = requests.Session()
        session.trust_env = False
        response = session.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
        response.raise_for_status()
        payload = response.json()
        result = payload.get("chart", {}).get("result", [])
        if not result:
            return pd.DataFrame()

        chart = result[0]
        timestamps = chart.get("timestamp") or []
        quote_data = chart.get("indicators", {}).get("quote", [{}])[0]
        if not timestamps or not quote_data:
            return pd.DataFrame()

        data = pd.DataFrame(
            {
                "Date": pd.to_datetime(timestamps, unit="s").date,
                "Open": quote_data.get("open"),
                "High": quote_data.get("high"),
                "Low": quote_data.get("low"),
                "Close": quote_data.get("close"),
                "Volume": quote_data.get("volume"),
            }
        )
        data = data.dropna(subset=["Open", "High", "Low", "Close", "Volume"])
        if data.empty:
            return pd.DataFrame()

        return prepare_market_data(data.set_index("Date"))
    except Exception:
        return pd.DataFrame()


def fetch_stock_data(ticker: str, period: str, interval: str) -> pd.DataFrame:
    prepared_data = fetch_yahoo_chart_data(ticker, period, interval)
    if not prepared_data.empty:
        return prepared_data

    try:
        data = yf.download(ticker, period=period, interval=interval, auto_adjust=True, progress=False)
    except Exception:
        data = pd.DataFrame()

    return prepare_market_data(data)


def read_stock_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    try:
        data = pd.read_csv(path, parse_dates=["Date"], index_col="Date")
    except Exception:
        return pd.DataFrame()
    return prepare_market_data(data)


def load_stock_data(ticker: str, period: str, interval: str, refresh: bool) -> pd.DataFrame:
    cache_path = market_csv_path(ticker, period, interval)
    if refresh:
        fetched_data = fetch_stock_data(ticker, period, interval)
        if not fetched_data.empty:
            fetched_data.to_csv(cache_path)
            cached = read_stock_csv(cache_path)
            if not cached.empty:
                return cached

    cached_data = read_stock_csv(cache_path)
    if not cached_data.empty:
        return cached_data

    legacy_cached_data = read_stock_csv(LEGACY_MARKET_CSV_PATH)
    if not refresh and not legacy_cached_data.empty:
        return legacy_cached_data

    return pd.DataFrame()
