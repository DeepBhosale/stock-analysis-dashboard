from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from stock_analysis import analyze_ticker, fetch_live_watchlist_data

app = FastAPI(title="Stock Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    ticker: str
    period: str
    interval: str
    refresh: bool = True


class WatchlistResponse(BaseModel):
    ticker: str
    name: str
    price: str
    change: str
    finalSignal: str
    marketTrend: str
    bullishProbability: int
    riskScore: int
    notes: str


@app.post("/api/analyze")
def analyze(request: AnalyzeRequest):
    try:
        result = analyze_ticker(request.ticker, request.period, request.interval, request.refresh)
        return result
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Server error: {exc}")


@app.get("/api/watchlist", response_model=list[WatchlistResponse])
def watchlist():
    tickers = ["AAPL", "MSFT", "TSLA", "NVDA", "AMZN"]
    try:
        live_data = fetch_live_watchlist_data(tickers)
        return live_data
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Server error: {exc}")
