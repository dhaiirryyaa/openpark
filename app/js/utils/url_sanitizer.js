export function sanitizeUrlParams(paramsObj) {
  const clean = {};
  for (const [k, v] of Object.entries(paramsObj)) {
    if (v !== undefined && v !== null && v !== '') {
      clean[encodeURIComponent(k)] = encodeURIComponent(String(v));
    }
  }
  return clean;
}
