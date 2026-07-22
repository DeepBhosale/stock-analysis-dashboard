interface InputPageProps {
  ticker: string
  refresh: boolean
  loading: boolean
  error: string | null
  period: string
  interval: string
  onTickerChange: (ticker: string) => void
  onRefreshChange: (refresh: boolean) => void
  onAnalyze: () => void
}

export function InputPage({
  ticker,
  refresh,
  loading,
  error,
  period,
  interval,
  onTickerChange,
  onRefreshChange,
  onAnalyze,
}: InputPageProps) {
  return (
    <section className="controls-card">
      <div className="section-header">
        <div>
          <span className="section-kicker">Ticker analysis</span>
          <h2>Run a market signal</h2>
        </div>
      </div>
      <div className="field-group">
        <label>Ticker</label>
        <input value={ticker} onChange={event => onTickerChange(event.target.value)} placeholder="AAPL" />
      </div>
      <div className="field-group checkbox-field">
        <label>
          <input
            type="checkbox"
            checked={refresh}
            onChange={event => onRefreshChange(event.target.checked)}
          />
          Refresh data from yfinance
        </label>
      </div>
      <div className="fixed-info">
        <div>
          <span>Period</span>
          <strong>{period}</strong>
        </div>
        <div>
          <span>Interval</span>
          <strong>{interval}</strong>
        </div>
      </div>
      <button onClick={onAnalyze} disabled={loading}>
        {loading ? 'Analyzing...' : 'Analyze'}
      </button>
      {error && <div className="error-box">{error}</div>}
    </section>
  )
}
