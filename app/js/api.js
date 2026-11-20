// api.js – OpenPark Clean Unified Backend Client
export const API = {
  async getNearbyLots(lat, lon, filter = 'all') {
    try {
      let url = `/lots/nearby?lat=${lat}&lon=${lon}&radius=4000`;
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      let lots = await res.json();
      if (!Array.isArray(lots)) lots = [];

      if (filter === 'Available') {
        lots = lots.filter((l) => l.status === 'Available' || (l.free_spots || 0) > 0);
      } else if (filter === 'ev') {
        lots = lots.filter((l) => l.is_ev || (l.name || '').toLowerCase().includes('ev'));
      } else if (filter === 'budget') {
        lots = lots.filter((l) => {
          const p = parseInt(String(l.price_car || '').replace(/[^0-9]/g, ''), 10);
          return isNaN(p) || p <= 30;
        });
      } else if (filter === 'covered') {
        lots = lots.filter((l) => l.is_covered || (l.name || '').toLowerCase().includes('covered') || (l.name || '').toLowerCase().includes('basement'));
      }
      return lots;
    } catch (err) {
      console.warn('[API] getNearbyLots fallback to /api/lots:', err);
      try {
        const fallback = await fetch('/api/lots');
        if (fallback.ok) return await fallback.json();
      } catch {}
      return [];
    }
  },

  async searchPlaces(query, centerLat, centerLon) {
    if (!query || query.trim().length < 2) return [];
    const q = encodeURIComponent(query.trim());
    try {
      let url = `/api/places/search?q=${q}`;
      if (Number.isFinite(centerLat) && Number.isFinite(centerLon)) {
        url += `&lat=${centerLat}&lon=${centerLon}`;
      }
      const res = await fetch(url);
      if (res.ok) {
        const data = await res.json();
        return Array.isArray(data) ? data : (data.results || []);
      }
    } catch (e) {
      console.warn('[API] places/search failed, trying traccar:', e);
    }

    try {
      const res = await fetch(`/api/traccar/search?q=${q}`);
      if (res.ok) {
        const data = await res.json();
        return Array.isArray(data) ? data : (data.results || []);
      }
    } catch {}
    return [];
  },

  async getRoute(startLat, startLon, endLat, endLon) {
    try {
      const res = await fetch(`/api/traccar/route?start_lat=${startLat}&start_lon=${startLon}&end_lat=${endLat}&end_lon=${endLon}`);
      if (res.ok) {
        return await res.json();
      }
    } catch (err) {
      console.warn('[API] route fetch failed:', err);
    }
    // Fallback: direct line coordinates
    return {
      coordinates: [[startLon, startLat], [endLon, endLat]],
      distance_km: 1.2,
      duration_mins: 4,
      steps: [{ instruction: 'Head toward destination', distance_m: 1200 }]
    };
  },

  async holdBay(lotId) {
    try {
      const res = await fetch(`/lots/${lotId}/hold`, { method: 'POST' });
      return res.ok ? await res.json() : null;
    } catch (e) {
      return null;
    }
  },

  async releaseHold(lotId) {
    try {
      const res = await fetch(`/lots/${lotId}/hold`, { method: 'DELETE' });
      return res.ok;
    } catch (e) {
      return false;
    }
  }
};
