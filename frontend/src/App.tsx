import { useEffect, useState } from 'react'

import { Sidebar } from './components/Sidebar'
import { Toolbar } from './components/Toolbar'
import { AnalysisPage } from './pages/AnalysisPage'
import { InputPage } from './pages/InputPage'
import { LivePage } from './pages/LivePage'
import type { AnalyzeResponse, Page, WatchlistItem } from './types'

function App() {
  const [ticker, setTicker] = useState('AAPL')
  const [refresh, setRefresh] = useState(true)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<AnalyzeResponse | null>(null)
  const [activePage, setActivePage] = useState<Page>('input')
  const [expandedTicker, setExpandedTicker] = useState<string | null>(null)
  const [watchlist, setWatchlist] = useState<WatchlistItem[]>([])
  const [watchlistLoading, setWatchlistLoading] = useState(false)
  const [watchlistError, setWatchlistError] = useState<string | null>(null)
  const [watchlistUpdatedAt, setWatchlistUpdatedAt] = useState<string | null>(null)
  const period = '5y'
  const interval = '1d'

  const fetchWatchlist = async () => {
    setWatchlistLoading(true)
    setWatchlistError(null)
    try {
      const response = await fetch('http://localhost:8000/api/watchlist')
      if (!response.ok) {
        const payload = await response.json()
        throw new Error(payload.detail || 'Request failed')
      }
      const data = (await response.json()) as WatchlistItem[]
      setWatchlist(data)
      setWatchlistUpdatedAt(new Date().toLocaleTimeString())
    } catch (err) {
      setWatchlistError((err as Error).message)
    } finally {
      setWatchlistLoading(false)
    }
  }

  useEffect(() => {
    fetchWatchlist()
    const intervalId = window.setInterval(fetchWatchlist, 30000)
    return () => window.clearInterval(intervalId)
  }, [])

  const analyze = async (selectedTicker = ticker) => {
    const cleanTicker = selectedTicker.trim().toUpperCase()
    if (!cleanTicker) {
      setError('Enter a ticker symbol first.')
      return
    }

    setTicker(cleanTicker)
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ticker: cleanTicker, period, interval, refresh }),
      })
      if (!response.ok) {
        const payload = await response.json()
        throw new Error(payload.detail || 'Request failed')
      }
      const data = (await response.json()) as AnalyzeResponse
      setResult(data)
      setActivePage('analysis')
    } catch (err) {
      setError((err as Error).message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app-shell">
      <Toolbar period={period} interval={interval} />

      <main className="main-layout">
        <Sidebar activePage={activePage} onPageChange={setActivePage} />

        <div className="main-area">
          {activePage === 'input' && (
            <InputPage
              ticker={ticker}
              refresh={refresh}
              loading={loading}
              error={error}
              period={period}
              interval={interval}
              onTickerChange={setTicker}
              onRefreshChange={setRefresh}
              onAnalyze={() => analyze()}
            />
          )}

          {activePage === 'live' && (
            <LivePage
              ticker={ticker}
              loading={loading}
              watchlist={watchlist}
              watchlistLoading={watchlistLoading}
              watchlistError={watchlistError}
              watchlistUpdatedAt={watchlistUpdatedAt}
              expandedTicker={expandedTicker}
              onRefreshWatchlist={fetchWatchlist}
              onExpandedTickerChange={setExpandedTicker}
              onAnalyze={analyze}
            />
          )}

          {activePage === 'analysis' && <AnalysisPage result={result} />}
        </div>
      </main>
    </div>
  )
}

export default App
