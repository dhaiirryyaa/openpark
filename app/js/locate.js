// locate.js – honest "where am I" for OpenPark.
// Rule: the map only moves when we have a REAL fix. No default spot, no IP guess, no random lot.
// Coordinates: browser gives {latitude, longitude}; MapLibre wants [lon, lat].

export const LOC = (typeof window !== 'undefined' && window.__openpark_loc) || {
  state: 'idle',
  lat: null,
  lon: null,
  accuracy: null,
  ts: 0
};
if (typeof window !== 'undefined') {
  window.__openpark_loc = LOC;
}

const listeners = (typeof window !== 'undefined' && window.__openpark_loc_listeners) || new Set();
if (typeof window !== 'undefined') {
  window.__openpark_loc_listeners = listeners;
}

export const onLocation = (fn) => {
  listeners.add(fn);
  if (LOC.lat != null && LOC.lon != null) {
    try { fn({ ...LOC }); } catch (e) { console.error('[locate] listener error:', e); }
  }
  return () => listeners.delete(fn);
};

const set = (patch) => {
  Object.assign(LOC, patch);
  listeners.forEach((f) => {
    try { f({ ...LOC }); } catch (e) { console.error('[locate] listener error:', e); }
  });
};

let watchId = null;

export async function startLocating({ timeoutMs = 15000 } = {}) {
  if (!('geolocation' in navigator)) return set({ state: 'unavailable' });
  if (!window.isSecureContext) return set({ state: 'insecure' }); // geolocation needs HTTPS or localhost

  try { // react if the user flips the permission in browser settings
    const perm = await navigator.permissions?.query({ name: 'geolocation' });
    if (perm) {
      perm.onchange = () => {
        if (perm.state === 'granted') startLocating();
        else if (perm.state === 'denied') set({ state: 'denied' });
      };
    }
  } catch { /* Permissions API not available (older Safari) – fine */ }

  set({ state: 'locating' });
  if (watchId != null) {
    navigator.geolocation.clearWatch(watchId);
    watchId = null;
  }

  const ok = (p) => {
    const { latitude: lat, longitude: lon, accuracy } = p.coords;
    if (!Number.isFinite(lat) || !Number.isFinite(lon)) return;
    const now = p.timestamp || Date.now();

    // Strict Device Fix Filter:
    // Reject coarse IP or cellular tower estimates (> 200m).
    // The user's device live GPS / Wi-Fi fix must be accurate to <= 200m.
    if (accuracy > 200) {
      console.warn(`[GPS] Coarse location reading rejected (±${Math.round(accuracy)}m). Waiting for real hardware GPS fix.`);
      return;
    }

    // Prevent degradation: if we already have a recent high-accuracy fix, reject sudden jumps to poorer accuracy
    if (LOC.lat != null && LOC.accuracy != null && (now - LOC.ts < 30000)) {
      if (accuracy > LOC.accuracy * 2 && accuracy > 80) {
        return;
      }
    }

    set({ state: accuracy <= 60 ? 'precise' : 'acceptable', lat, lon, accuracy, ts: now });
  };

  const fail = (e) => {
    if (LOC.lat == null) {
      set({ state: e.code === 1 ? 'denied' : e.code === 2 ? 'unavailable' : 'timeout' });
    }
  };

  // 1) Fast hardware GNSS / Wi-Fi fix (enableHighAccuracy: true, maximumAge: 0 forces real device coordinates, NEVER IP lookup)
  navigator.geolocation.getCurrentPosition(ok, (e) => {
    if (e.code === 1) return fail(e);
    // If initial query timed out, retry with high accuracy and longer timeout (never fall back to coarse IP)
    navigator.geolocation.getCurrentPosition(ok, fail, { enableHighAccuracy: true, timeout: timeoutMs, maximumAge: 0 });
  }, { enableHighAccuracy: true, timeout: Math.min(timeoutMs, 8000), maximumAge: 0 });

  // 2) Keep refining continuously via watchPosition with high accuracy hardware GNSS
  watchId = navigator.geolocation.watchPosition(ok, (e) => {
    if (e.code === 1) fail(e);
  }, { enableHighAccuracy: true, maximumAge: 0, timeout: 20000 });
}

export function stopLocating() {
  if (watchId != null) {
    navigator.geolocation.clearWatch(watchId);
    watchId = null;
  }
}

export const LOCATION_MESSAGES = {
  locating: 'Finding your location…',
  precise: 'Live GPS active',
  acceptable: 'Live GPS active',
  denied: 'Location access is blocked. Allow it in your browser’s site settings.',
  unavailable: 'Couldn’t get a location fix. Turn on device location or Wi-Fi.',
  timeout: 'GPS fix taking longer than expected. Retrying…',
  insecure: 'Location requires a secure (HTTPS) connection.',
};

if (typeof window !== 'undefined') {
  window.OpenParkLocate = {
    LOC,
    onLocation,
    startLocating,
    stopLocating,
    LOCATION_MESSAGES
  };
  window.LOC = LOC;
}
