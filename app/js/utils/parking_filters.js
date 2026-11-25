export function filterParkingLots(lots, criteria = {}) {
  return lots.filter(lot => {
    if (criteria.evOnly && !lot.has_ev) return false;
    if (criteria.coveredOnly && !lot.is_covered) return false;
    if (criteria.maxPrice && (lot.price_hourly || 0) > criteria.maxPrice) return false;
    if (criteria.minFreeBays && (lot.free_spots || 0) < criteria.minFreeBays) return false;
    return true;
  });
}
