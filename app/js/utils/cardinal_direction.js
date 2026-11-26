export function degreesToCardinal(deg) {
  const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
  const normalized = (deg % 360 + 360) % 360;
  const idx = Math.round(normalized / 45) % 8;
  return directions[idx];
}
