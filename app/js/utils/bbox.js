export function expandBoundingBox(bbox, marginKm = 0.5) {
  const deltaLat = marginKm / 111.0;
  const deltaLon = marginKm / (111.0 * Math.cos((bbox.minLat * Math.PI) / 180.0));
  return {
    minLat: bbox.minLat - deltaLat,
    maxLat: bbox.maxLat + deltaLat,
    minLon: bbox.minLon - deltaLon,
    maxLon: bbox.maxLon + deltaLon
  };
}
