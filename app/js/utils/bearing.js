export function calculateBearingDelta(b1, b2) {
  let diff = (b2 - b1 + 180) % 360 - 180;
  return diff < -180 ? diff + 360 : diff;
}
