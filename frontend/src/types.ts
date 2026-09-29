export interface AnalyzeResponse {
  ticker: string;
  finalSignal: string;
  weightedScore: number;
  marketTrend: string;
  lstmTrend: string;
  lstmMovePct: number;
  bullishProbability: number;
  riskScore: number;
  xgbOutlook: string;
  priceChangePct: number;
  rows: number;
  accuracy: number;
  signalReasons: string[];
  indicatorReasons: string[];
  chartData: {
    dates: string[];
    open: number[];
    high: number[];
    low: number[];
    close: number[];
    sma20: number[];
    sma50: number[];
    rsi: number[];
    macd: number[];
    macdSignal: number[];
    macdHist: number[];
  };
}

export interface WatchlistItem {
  ticker: string;
  name: string;
  price: string;
  change: string;
  finalSignal: string;
  marketTrend: string;
  bullishProbability: number;
  riskScore: number;
  notes: string;
}

export type Page = 'input' | 'live' | 'analysis';