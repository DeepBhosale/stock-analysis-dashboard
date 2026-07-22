import { PriceChart } from '../components/PriceChart'
import type { AnalyzeResponse } from '../types'
import { signalTone } from '../utils/signals'

interface AnalysisPageProps {
  result: AnalyzeResponse | null
}

export function AnalysisPage({ result }: AnalysisPageProps) {
  return (
    <section className="results-card">
      <div className="section-header">
        <div>
          <span className="section-kicker">Model output</span>
          <h2>{result ? `${result.ticker} analysis` : 'Analysis'}</h2>
        </div>
      </div>
      {!result ? (
        <div className="placeholder-card">
          <h3>No analysis yet</h3>
        </div>
      ) : (
        <>
          <div className="metrics-grid">
            <div className="metric-card">
              <span className="metric-label">Final Signal</span>
              <strong className={`metric-value ${signalTone(result.finalSignal)}`}>{result.finalSignal}</strong>
            </div>
            <div className="metric-card">
              <span className="metric-label">Market Trend</span>
              <strong className={`metric-value ${signalTone(result.marketTrend)}`}>{result.marketTrend}</strong>
            </div>
            <div className="metric-card">
              <span className="metric-label">XGBoost</span>
              <strong className={`metric-value ${signalTone(result.xgbOutlook)}`}>{result.xgbOutlook}</strong>
            </div>
            <div className="metric-card">
              <span className="metric-label">Bullish Probability</span>
              <strong>{result.bullishProbability}%</strong>
            </div>
            <div className="metric-card">
              <span className="metric-label">LSTM Trend</span>
              <strong>{result.lstmTrend} ({result.lstmMovePct}%)</strong>
            </div>
            <div className="metric-card">
              <span className="metric-label">Risk Score</span>
              <strong>{result.riskScore}/100</strong>
            </div>
          </div>

          <div className="summary-block">
            <div>
              <span>Rows used</span>
              <strong>{result.rows}</strong>
            </div>
            <div>
              <span>XGBoost test accuracy</span>
              <strong>{result.accuracy}%</strong>
            </div>
          </div>

          <div className="reasons-grid">
            <article>
              <h3>Signal reasons</h3>
              <ul>
                {result.signalReasons.map(reason => <li key={reason}>{reason}</li>)}
              </ul>
            </article>
            <article>
              <h3>Indicator reasons</h3>
              <ul>
                {result.indicatorReasons.map(reason => <li key={reason}>{reason}</li>)}
              </ul>
            </article>
          </div>

          <PriceChart chartData={result.chartData} />
        </>
      )}
    </section>
  )
}
