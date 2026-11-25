export function classifyGeolocationError(err) {
  if (!err) return { code: 0, userMsg: 'Location acquired' };
  switch (err.code) {
    case 1: return { code: 1, userMsg: 'GPS permission denied. Enable location in settings.' };
    case 2: return { code: 2, userMsg: 'GPS position unavailable. Check device antenna.' };
    case 3: return { code: 3, userMsg: 'GPS fix timed out. Retrying with network location.' };
    default: return { code: 4, userMsg: err.message || 'GPS lookup failed.' };
  }
}
