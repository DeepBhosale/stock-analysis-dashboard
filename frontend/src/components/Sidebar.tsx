import type { Page } from '../types'

interface SidebarProps {
  activePage: Page
  onPageChange: (page: Page) => void
}

export function Sidebar({ activePage, onPageChange }: SidebarProps) {
  return (
    <aside className="sidebar">
      <div className="sidebar-card">
        <div className="brand-panel">
          <span className="brand-mark">SA</span>
          <div>
            <strong>Analysis Desk</strong>
            <small>FastAPI + React</small>
          </div>
        </div>
        <div className="sidebar-nav">
          <button className={activePage === 'input' ? 'active' : ''} onClick={() => onPageChange('input')}>
            Input
          </button>
          <button className={activePage === 'live' ? 'active' : ''} onClick={() => onPageChange('live')}>
            Live updates
          </button>
          <button className={activePage === 'analysis' ? 'active' : ''} onClick={() => onPageChange('analysis')}>
            Analysis
          </button>
        </div>
      </div>
    </aside>
  )
}
