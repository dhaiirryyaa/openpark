export function formatRemainingHoldTime(expiresAtMs) {
  const diff = Math.max(0, expiresAtMs - Date.now());
  const totalSecs = Math.floor(diff / 1000);
  const m = Math.floor(totalSecs / 60);
  const s = totalSecs % 60;
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
}
