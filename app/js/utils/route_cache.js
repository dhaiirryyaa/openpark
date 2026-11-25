export class OfflineRouteCache {
  constructor() {
    this.cacheKey = 'openpark_cached_routes_v1';
  }
  save(origin, dest, routeData) {
    try {
      const key = `${origin.lat.toFixed(3)},${origin.lon.toFixed(3)}_${dest.lat.toFixed(3)},${dest.lon.toFixed(3)}`;
      const existing = JSON.parse(localStorage.getItem(this.cacheKey) || '{}');
      existing[key] = { data: routeData, cachedAt: Date.now() };
      localStorage.setItem(this.cacheKey, JSON.stringify(existing));
    } catch (e) {}
  }
}
