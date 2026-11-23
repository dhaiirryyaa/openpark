/** Network Status Observer */
export function initNetworkObserver(onStatusChange) {
  window.addEventListener('online', () => onStatusChange(true));
  window.addEventListener('offline', () => onStatusChange(false));
  return navigator.onLine;
}
