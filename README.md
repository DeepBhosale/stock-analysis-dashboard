# AI Stock Analysis Dashboard

This project now runs as a React + Vite frontend with a FastAPI backend.

## Backend Setup

```powershell
cd backend
python -m venv .venv-backend
.\.venv-backend\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run Backend

```powershell
.\start-backend.ps1
```

## Frontend Setup

```powershell
cd frontend
npm install
```

## One-Time Setup

After unzipping the project on a new computer, run:

```powershell
.\setup.ps1
```

This creates the backend virtual environment and installs frontend dependencies.

## Run Frontend

```powershell
.\start-frontend.ps1
```

Open the Vite URL shown in the terminal.

## Run Everything

```powershell
.\start-all.ps1
```

This opens backend and frontend in separate PowerShell windows.

## Notes

- The frontend calls `http://localhost:8000/api/analyze`
- The backend uses `data/market_data.csv` as its shared cache file
- This dashboard is educational and not financial advice

## Backend Library Structure

The backend analysis code is organized as an internal Python library under `backend/stock_analysis/`:

- `data_fetcher.py` fetches Yahoo Finance data and manages CSV cache files
- `indicators.py` calculates technical indicators and chart data
- `ml_models.py` trains the XGBoost and LSTM models
- `signals.py` combines model, trend, and risk output into final signals
- `risk.py` calculates risk scores
- `watchlist.py` builds live watchlist rows
- `service.py` runs the full ticker analysis workflow

## Frontend Structure

The React UI is organized under `frontend/src/`:

- `App.tsx` owns top-level state, API calls, and page switching
- `components/` contains shared UI pieces like the toolbar, sidebar, and chart
- `pages/` contains the Input, Live Watchlist, and Analysis screens
- `utils/` contains chart and signal helper functions
- `types.ts` contains shared TypeScript types
