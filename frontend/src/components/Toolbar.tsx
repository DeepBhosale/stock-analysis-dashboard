interface ToolbarProps {
  period: string
  interval: string
}

export function Toolbar({ period, interval }: ToolbarProps) {
  return (
    <header className="toolbar">
      <div>
        <h1>Stock Analytics</h1>
        <p>AI-assisted market signal dashboard</p>
      </div>
      <div className="toolbar-meta">
        <span>Period {period}</span>
        <span>Interval {interval}</span>
      </div>
    </header>
  )
}
