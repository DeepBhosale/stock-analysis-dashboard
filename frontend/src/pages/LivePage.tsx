import type { WatchlistItem } from '../types'
import { signalTone } from '../utils/signals'

interface LivePageProps {
  ticker: string
  loading: boolean
  watchlist: WatchlistItem[]
  watchlistLoading: boolean
  watchlistError: string | null
  watchlistUpdatedAt: string | null
  expandedTicker: string | null
  onRefreshWatchlist: () => void
  onExpandedTickerChange: (ticker: string | null) => void
  onAnalyze: (ticker: string) => void
}

export function LivePage({
  ticker,
  loading,
  watchlist,
  watchlistLoading,
  watchlistError,
  watchlistUpdatedAt,
  expandedTicker,
  onRefreshWatchlist,
  onExpandedTickerChange,
  onAnalyze,
}: LivePageProps) {
  return (
    <section className="results-card">
      <div className="section-header">
        <div>
          <span className="section-kicker">Watchlist</span>
          <h2>Live market snapshot</h2>
        </div>
        <button onClick={onRefreshWatchlist} disabled={watchlistLoading}>
          {watchlistLoading ? 'Refreshing...' : 'Refresh now'}
        </button>
      </div>
      <div className="live-actions">
        {watchlistUpdatedAt && <span>Updated {watchlistUpdatedAt}</span>}
      </div>
      {watchlistLoading && <div className="status-box">Refreshing watchlist...</div>}
      {watchlistError && <div className="error-box">{watchlistError}</div>}
      {!watchlistLoading && !watchlistError && watchlist.length === 0 && (
        <div className="status-box">No live rows returned yet. Try Refresh now.</div>
      )}
      <div className="watchlist-card">
        {watchlist.map(stock => {
          const expanded = expandedTicker === stock.ticker
          const chartUrl = `https://www.tradingview.com/symbols/${stock.ticker}/`
          return (
            <div key={stock.ticker} className="watchlist-item">
              <div
                className="watchlist-header"
                onClick={() => onExpandedTickerChange(expanded ? null : stock.ticker)}
              >
                <div>
                  <strong>{stock.ticker}</strong>
                  <div>{stock.name}</div>
                </div>
                <div className="watchlist-summary">
                  <div className={stock.change.startsWith('+') ? 'positive' : 'negative'}>
                    <span>{stock.price}</span>
                    <small>{stock.change}</small>
                  </div>
                  <span className={`signal-pill ${signalTone(stock.finalSignal)}`}>
                    {stock.finalSignal}
                  </span>
                  <a
                    href={chartUrl}
                    className="live-chart-button"
                    target="_blank"
                    rel="noreferrer"
                    onClick={event => event.stopPropagation()}
                  >
                    Live chart
                  </a>
                </div>
              </div>
              {expanded && (
                <div className="watchlist-details">
                  <div className="detail-row">
                    <span>Signal</span>
                    <strong>{stock.finalSignal}</strong>
                  </div>
                  <div className="detail-row">
                    <span>Trend</span>
                    <strong>{stock.marketTrend}</strong>
                  </div>
                  <div className="detail-row">
                    <span>Bullish probability</span>
                    <strong>{stock.bullishProbability}%</strong>
                  </div>
                  <div className="detail-row">
                    <span>Risk score</span>
                    <strong>{stock.riskScore}/100</strong>
                  </div>
                  <p className="detail-notes"><strong>Model note</strong>: {stock.notes}</p>
                  <button
                    className="analyze-stock-button"
                    onClick={() => onAnalyze(stock.ticker)}
                    disabled={loading}
                  >
                    {loading && ticker === stock.ticker ? 'Analyzing...' : `Analyze ${stock.ticker}`}
                  </button>
                </div>
              )}
            </div>
          )
        })}
      </div>
    </section>
  )
}
