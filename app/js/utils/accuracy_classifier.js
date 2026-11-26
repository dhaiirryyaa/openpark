export function classifyGpsAccuracy(accuracyMeters) {
  if (accuracyMeters <= 8) return { rating: 'HIGH', color: '#22c55e' };
  if (accuracyMeters <= 25) return { rating: 'MEDIUM', color: '#eab308' };
  return { rating: 'LOW', color: '#ef4444' };
}
