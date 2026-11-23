/** Safe Storage Manager */
class MemoryStorage {
  constructor() { this.store = {}; }
  getItem(key) { return this.store[key] || null; }
  setItem(key, val) { this.store[key] = String(val); }
  removeItem(key) { delete this.store[key]; }
}

const safeStorage = (() => {
  try {
    const test = '__test__';
    window.localStorage.setItem(test, test);
    window.localStorage.removeItem(test);
    return window.localStorage;
  } catch (e) {
    return new MemoryStorage();
  }
})();

export default safeStorage;
