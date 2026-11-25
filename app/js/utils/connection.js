export function getNetworkProfile() {
  const conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  if (!conn) return { type: 'unknown', downlink: 10, rtt: 50, isMetered: false };
  return {
    type: conn.effectiveType || '4g',
    downlink: conn.downlink || 10,
    rtt: conn.rtt || 50,
    isMetered: conn.saveData || false
  };
}
