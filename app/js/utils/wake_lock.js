export class ScreenWakeLockManager {
  constructor() { this.sentinel = null; }
  async request() {
    if ('wakeLock' in navigator) {
      try { this.sentinel = await navigator.wakeLock.request('screen'); }
      catch (e) {}
    }
  }
  release() {
    if (this.sentinel) { this.sentinel.release(); this.sentinel = null; }
  }
}
