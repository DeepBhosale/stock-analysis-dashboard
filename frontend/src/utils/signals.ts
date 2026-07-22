export function signalTone(signal: string) {
  const normalized = signal.toLowerCase()
  if (normalized.includes('buy') || normalized === 'bullish' || normalized === 'uptrend') return 'positive'
  if (normalized.includes('sell') || normalized === 'bearish' || normalized === 'downtrend') return 'negative'
  return 'neutral'
}
