export function calculateTargetZoom(distKm) {
  if (distKm <= 0.5) return 17.5;
  if (distKm <= 1.5) return 16.0;
  if (distKm <= 5.0) return 14.5;
  if (distKm <= 15.0) return 12.5;
  return 11.0;
}
