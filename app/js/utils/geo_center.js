export function calculateBoundingCenter(coords) {
  if (!coords || coords.length === 0) return { lat: 0, lon: 0 };
  let sumLat = 0, sumLon = 0;
  for (const c of coords) {
    sumLat += (c.lat !== undefined ? c.lat : c[1]);
    sumLon += (c.lon !== undefined ? c.lon : (c.lng !== undefined ? c.lng : c[0]));
  }
  return { lat: sumLat / coords.length, lon: sumLon / coords.length };
}
