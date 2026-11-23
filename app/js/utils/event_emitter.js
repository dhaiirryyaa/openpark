/** Pub/Sub Event Bus */
export class EventEmitter {
  constructor() { this.events = {}; }
  on(event, listener) {
    if (!this.events[event]) this.events[event] = [];
    this.events[event].push(listener);
    return () => this.off(event, listener);
  }
  off(event, listener) {
    if (!this.events[event]) return;
    this.events[event] = this.events[event].filter(l => l !== listener);
  }
  emit(event, data) {
    if (!this.events[event]) return;
    this.events[event].forEach(l => l(data));
  }
}
