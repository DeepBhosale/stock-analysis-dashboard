import type { AnalyzeResponse } from '../types'
import { renderArea, renderPath } from '../utils/chart'

export function PriceChart({ chartData }: { chartData: AnalyzeResponse['chartData'] }) {
  const len = Math.min(chartData.dates.length, 100)
  const dates = chartData.dates.slice(-len)
  const close = chartData.close.slice(-len)
  const sma20 = chartData.sma20.slice(-len)
  const sma50 = chartData.sma50.slice(-len)
  const macd = chartData.macd.slice(-len)
  const macdSignal = chartData.macdSignal.slice(-len)
  const macdHist = chartData.macdHist.slice(-len)

  const priceValues = [...close, ...sma20, ...sma50]
  const priceMax = Math.max(...priceValues)
  const priceMin = Math.min(...priceValues)
  const chartWidth = 900
  const chartHeight = 280
  const leftMargin = 56
  const rightMargin = 20
  const topMargin = 22
  const bottomMargin = 32
  const plotWidth = chartWidth - leftMargin - rightMargin
  const plotHeight = chartHeight - topMargin - bottomMargin
  const macdTop = chartHeight + 24
  const macdMax = Math.max(...macd, ...macdSignal, 0)
  const macdMin = Math.min(...macd, ...macdSignal, 0)
  const macdRange = macdMax - macdMin || 1
  const histHeight = 84
  const lineHeight = 84
  const panelGap = 20
  const macdLineTop = macdTop + histHeight + panelGap
  const histZeroY = macdTop + histHeight - ((0 - macdMin) / macdRange) * histHeight
  const lineZeroY = macdLineTop + lineHeight - ((0 - macdMin) / macdRange) * lineHeight

  const priceTicks = Array.from({ length: 5 }, (_, idx) => priceMax - (idx / 4) * (priceMax - priceMin))
  const dateTicks = Array.from({ length: 5 }, (_, idx) => {
    const index = Math.floor((idx / 4) * (len - 1))
    return { index, label: dates[index] }
  })

  return (
    <div className="chart-card">
      <div className="chart-header">
        <div>
          <span className="section-kicker">Technical chart</span>
          <h3>Price, SMA and MACD</h3>
        </div>
      </div>
      <svg viewBox={`0 0 ${chartWidth} ${chartHeight + histHeight + lineHeight + panelGap + 40}`} className="chart-svg">
        <defs>
          <linearGradient id="priceAreaGradient" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor="#2563eb" stopOpacity="0.18" />
            <stop offset="100%" stopColor="#2563eb" stopOpacity="0" />
          </linearGradient>
        </defs>

        {priceTicks.map((value, index) => {
          const y = topMargin + (index / 4) * plotHeight
          return (
            <g key={index}>
              <line x1={leftMargin} y1={y} x2={chartWidth - rightMargin} y2={y} stroke="#e2e8f0" strokeDasharray="4 4" />
              <text x={leftMargin - 10} y={y + 4} textAnchor="end" fontSize="11" fill="#6b7280">
                {value.toFixed(2)}
              </text>
            </g>
          )
        })}

        <path d={renderArea(close, priceMin, priceMax, plotWidth, plotHeight, leftMargin, topMargin)} fill="url(#priceAreaGradient)" />
        <path d={renderPath(close, priceMin, priceMax, plotWidth, plotHeight, leftMargin, topMargin)} fill="none" stroke="#2563eb" strokeWidth="2.5" strokeLinecap="round" />
        <path d={renderPath(sma20, priceMin, priceMax, plotWidth, plotHeight, leftMargin, topMargin)} fill="none" stroke="#0f766e" strokeWidth="1.75" strokeDasharray="8 4" strokeLinecap="round" />
        <path d={renderPath(sma50, priceMin, priceMax, plotWidth, plotHeight, leftMargin, topMargin)} fill="none" stroke="#f97316" strokeWidth="1.75" strokeDasharray="8 4" strokeLinecap="round" />

        {dateTicks.map(({ index, label }) => {
          const x = leftMargin + (index / (len - 1)) * plotWidth
          return (
            <g key={label}>
              <line x1={x} y1={chartHeight - bottomMargin + 4} x2={x} y2={chartHeight - bottomMargin + 10} stroke="#cbd5e1" />
              <text x={x} y={chartHeight - 8} textAnchor="middle" fontSize="10" fill="#6b7280">
                {label}
              </text>
            </g>
          )
        })}

        <line x1={leftMargin} y1={topMargin} x2={leftMargin} y2={topMargin + plotHeight} stroke="#cbd5e1" />
        <line x1={leftMargin} y1={topMargin + plotHeight} x2={chartWidth - rightMargin} y2={topMargin + plotHeight} stroke="#cbd5e1" />

        <g>
          <text x={leftMargin} y={macdTop - 8} fontSize="11" fill="#374151">MACD histogram</text>
          <rect x={leftMargin} y={macdTop} width={plotWidth} height={histHeight} fill="#f8fafc" rx="14" />
          {macdHist.map((value, index) => {
            const x = leftMargin + (index / (len - 1)) * plotWidth
            const barWidth = Math.max(2, plotWidth / len - 1)
            const y = macdTop + histHeight - ((value - macdMin) / macdRange) * histHeight
            return (
              <rect
                key={index}
                x={x - barWidth / 2}
                y={Math.min(y, histZeroY)}
                width={barWidth}
                height={Math.max(1, Math.abs(y - histZeroY))}
                fill={value >= 0 ? '#16a34a' : '#dc2626'}
                opacity={0.75}
                rx={1}
              />
            )
          })}
          <line x1={leftMargin} y1={histZeroY} x2={chartWidth - rightMargin} y2={histZeroY} stroke="#94a3b8" strokeDasharray="4 4" />
        </g>

        <g>
          <text x={leftMargin} y={macdLineTop - 8} fontSize="11" fill="#374151">MACD lines</text>
          <rect x={leftMargin} y={macdLineTop} width={plotWidth} height={lineHeight} fill="#f8fafc" rx="14" />
          <line x1={leftMargin} y1={lineZeroY} x2={chartWidth - rightMargin} y2={lineZeroY} stroke="#94a3b8" strokeDasharray="4 4" />
          <path d={renderPath(macd, macdMin, macdMax, plotWidth, lineHeight, leftMargin, macdLineTop)} fill="none" stroke="#0f766e" strokeWidth="1.75" strokeLinecap="round" />
          <path d={renderPath(macdSignal, macdMin, macdMax, plotWidth, lineHeight, leftMargin, macdLineTop)} fill="none" stroke="#dc2626" strokeWidth="1.75" strokeLinecap="round" />
        </g>
      </svg>
      <div className="chart-legend">
        <span><strong>Close price</strong></span>
        <span className="legend-line close-line" />
        <span><strong>SMA 20</strong></span>
        <span className="legend-line sma20-line" />
        <span><strong>SMA 50</strong></span>
        <span className="legend-line sma50-line" />
      </div>
      <div className="chart-legend">
        <span><strong>MACD</strong></span>
        <span className="legend-line macd-line" />
        <span><strong>MACD signal</strong></span>
        <span className="legend-line macd-signal-line" />
      </div>
    </div>
  )
}
