export function estimateCrosstrackError(lat, lon, lineStart, lineEnd) {
  const d13 = Math.hypot(lat - lineStart.lat, lon - lineStart.lon) * 111320;
  return Math.abs(d13);
}
