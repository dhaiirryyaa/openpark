// locate.js – honest "where am I" for OpenPark.
// Rule: the map only moves when we have a REAL fix. No default spot, no IP guess, no random lot.
// Coordinates: browser gives {latitude, longitude}; MapLibre wants [lon, lat].

export const LOC = { state: 'idle', lat: null, lon: null, accuracy: null, ts: 0 };
// state: idle | locating | precise (<=100 m) | coarse (>100 m) | denied | unavailable | timeout | insecure
const listeners = new Set();
export const onLocation = (fn) => { listeners.add(fn); return () => listeners.delete(fn); };
const set = (patch) => { Object.assign(LOC, patch); listeners.forEach((f) => f({ ...LOC })); };

let watchId = null;

export async function startLocating({ timeoutMs = 12000 } = {}) {
  if (!('geolocation' in navigator)) return set({ state: 'unavailable' });
  if (!window.isSecureContext) return set({ state: 'insecure' }); // geolocation needs HTTPS or localhost

  try { // react if the user flips the permission in browser settings
    const perm = await navigator.permissions?.query({ name: 'geolocation' });
    if (perm) perm.onchange = () => (perm.state === 'granted' ? startLocating() : perm.state === 'denied' && set({ state: 'denied' }));
  } catch { /* Permissions API not available (older Safari) – fine */ }

  set({ state: 'locating' });
  if (watchId != null) navigator.geolocation.clearWatch(watchId);

  const ok = (p) => {
    const { latitude: lat, longitude: lon, accuracy } = p.coords;
    if (!Number.isFinite(lat) || !Number.isFinite(lon)) return;
    const now = p.timestamp || Date.now();
    // Prevent degradation: if we already have a recent high-accuracy fix, reject sudden jumps to coarse
    if (LOC.lat != null && LOC.accuracy != null && (now - LOC.ts < 45000)) {
      if (accuracy > LOC.accuracy * 2 && accuracy > 120) {
        return;
      }
    }
    // NOTE: no 40 m accuracy gate here. Laptops / indoor Wi-Fi give 100-2000 m, and rejecting
    // those is what makes an app "never find me". Show the accuracy instead; keep the strict filter for live tracking.
    set({ state: accuracy <= 100 ? 'precise' : 'coarse', lat, lon, accuracy, ts: now });
  };
  const fail = (e) => set({ state: e.code === 1 ? 'denied' : e.code === 2 ? 'unavailable' : 'timeout' });

  // 1) fast first answer, GPS preferred
  navigator.geolocation.getCurrentPosition(ok, (e) => {
    if (e.code === 1) return fail(e);
    // 2) retry once with network/Wi-Fi location (works on desktops without GPS)
    navigator.geolocation.getCurrentPosition(ok, fail, { enableHighAccuracy: false, timeout: timeoutMs, maximumAge: 60000 });
  }, { enableHighAccuracy: true, timeout: timeoutMs, maximumAge: 0 });

  // 3) keep refining; later fixes replace the first one (maximumAge: 0 prevents stale cache)
  watchId = navigator.geolocation.watchPosition(ok, (e) => { if (e.code === 1) fail(e); },
    { enableHighAccuracy: true, maximumAge: 0, timeout: 20000 });
}

export function stopLocating() {
  if (watchId != null) navigator.geolocation.clearWatch(watchId);
  watchId = null;
}

export const LOCATION_MESSAGES = {
  locating: 'Finding your location…',
  coarse: 'Location is approximate – step outside or enable GPS for better accuracy.',
  denied: 'Location is blocked. Allow it in your browser’s site settings, or search for a place.',
  unavailable: 'Couldn’t get a location fix. Turn on device location or search for a place.',
  timeout: 'Location is taking too long. Try again or search for a place.',
  insecure: 'Location needs a secure (HTTPS) connection.',
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
