export function calculateRoadGrade(riseMeters, runMeters) {
  if (runMeters <= 0) return 0;
  return Math.round((riseMeters / runMeters) * 100 * 10) / 10;
}
