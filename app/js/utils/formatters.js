/** Formatting Utilities */
export function formatCurrencyINR(amount) {
  return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(amount);
}

export function formatDurationMins(minutes) {
  if (minutes < 60) return `${Math.round(minutes)}m`;
  const hrs = Math.floor(minutes / 60);
  const mins = Math.round(minutes % 60);
  return `${hrs}h ${mins}m`;
}

export function formatDistanceKm(km) {
  return km < 1.0 ? `${Math.round(km * 1000)}m` : `${km.toFixed(1)} km`;
}
